import hashlib
# import logging
import traceback

import nmslib
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
#                     datefmt='%m/%d/%Y %H:%M:%S',
#                     level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class ClusterBuilder:

    def __init__(self, albert, embedder, batch_size, all_comments, all_data, all_sents, users):
        self.albert = albert
        self.embedder = embedder
        self.batch_size = batch_size
        self.all_comments = all_comments
        self.all_data = all_data
        self.all_sents = all_sents
        self.users = users

    def _get_best_head_avg_count(self, cluster_items):
        # logger.debug('_get_best_head_avg_count called')
        n = len(cluster_items)
        embeddings = [cluster_items[i][2] for i in range(n)]
        index = nmslib.init(method='hnsw', space='cosinesimil')
        index.addDataPointBatch(embeddings)
        index.createIndex(print_progress=True)
        max_avg_similarity = 0
        max_avg_similarity_i = 0

        for i in range(len(embeddings)):
            ids, distances = index.knnQuery(embeddings[i], k=n)
            avg_similarity = (n - sum(distances)) / n
            if avg_similarity > max_avg_similarity:
                max_avg_similarity = avg_similarity
                max_avg_similarity_i = i

        return cluster_items[max_avg_similarity_i][0], max_avg_similarity, n

    def _is_duplicate_cluster(self, cluster, sent):
        # logger.debug('_is_duplicate_cluster called')
        for item in cluster:
            if item == sent:
                return True

            for sent_id in cluster[item]:
                if sent == sent_id[0]:
                    return True

        return False

    def _get_answers_from_queries(self, query_list):
        # logger.debug('_get_answers_from_queries called')
        query_dic = {}
        for query in query_list:
            query_dic[query] = []
        
        reverse_sent_dic = {}  # index: sent-id
        all_sent_list = []
        i = 0
        for item in self.all_sents:
            reverse_sent_dic[i] = item
            all_sent_list.append(self.all_sents[item][0])
            i += 1

        i = 0
        offset = 0
        while i < len(all_sent_list):
            sents = all_sent_list[i:min(i + self.batch_size, len(all_sent_list))]
            try:
                predictions = self.albert.predict(query_list, sents)
                for pred in list(predictions):
                    if predictions[pred] != '':
                        # the id of the prediction is of the form 'sentid-qid'
                        id_split = pred.split('-')
                        sent_i, q_i = int(id_split[0]), int(id_split[1])
                        query_dic[query_list[q_i]].append(
                            (
                                predictions[pred],
                                self.embedder.get_embeddings([predictions[pred]]),
                                reverse_sent_dic[offset + sent_i]
                            )
                        )

                offset += self.batch_size
                i = min(i + self.batch_size, len(all_sent_list))

            except Exception as e:
                # logger.error(str(e))
                traceback.print_exc()

        return query_dic

    def _get_mini_clusters(self, embeddings, sents, orig_ids, min_similarity):
        # logger.debug('_get_mini_clusters called')
        index = nmslib.init(method='hnsw', space='cosinesimil')
        index.addDataPointBatch(embeddings)
        index.createIndex(print_progress=True)
        n = len(embeddings)
        good_clusters = {}
        orig_ids_str = ''.join([str(x) for x in orig_ids])
        hash_object = hashlib.md5(orig_ids_str.encode())
        orig_ids_str = str(hash_object.hexdigest())

        for i in range(len(embeddings)):
            ids, distances = index.knnQuery(embeddings[i], k=n)
            count = 0
            mini_cluster_ids = []

            for _id, dist in zip(ids, distances):
                if (1 - dist) >= min_similarity:
                    count += 1
                    mini_cluster_ids.append([sents[_id], orig_ids[_id], embeddings[_id]])

            if count >= 2:
                if not self._is_duplicate_cluster(good_clusters, sents[i]):
                    head, avg, count = self._get_best_head_avg_count(mini_cluster_ids)
                    good_clusters[head] = mini_cluster_ids

        return good_clusters

    def _get_best_clusters(self, labels, embeddings, answers, ids, min_similarity_start):
        """ids are sentence identifiers

        clusters is of the format:

            {
                0 : [ids],
                1 : [ids],
                .
                .
                n : [ids],
            }
        """
        # logger.debug('_get_best_clusters called')
        i = 0
        clusters = {}
        for item in labels:
            if item not in clusters:
                clusters[item] = []

            clusters[item].append(i)
            i += 1

        all_mini_clusters = {}
        for item in clusters:
            cluster_embeddings = []
            cluster_sents = []
            cluster_ids = []
            for it in clusters[item]:
                cluster_embeddings.append(embeddings[it])
                cluster_sents.append(answers[it])
                cluster_ids.append(ids[it])

            if len(cluster_embeddings) > 1:
                mini_clusters = self._get_mini_clusters(
                    cluster_embeddings,
                    cluster_sents,
                    cluster_ids,
                    min_similarity_start
                )

                for cluster in mini_clusters:
                    all_mini_clusters[cluster] = mini_clusters[cluster]

        return all_mini_clusters

    def _merge_clusters(self, full_cluster, max_clusters):
        # logger.debug('_merge_clusters called')
        keys = list(full_cluster.keys())
        embeddings = self.embedder.get_embeddings(keys)
        X = np.array(embeddings)
        clustering = AgglomerativeClustering(n_clusters=max_clusters).fit(X)
        labels = clustering.labels_
        clusters = {}
        i = 0
        for item in labels:
            if item not in clusters:
                clusters[item] = []

            clusters[item].extend(full_cluster[keys[i]])
            i += 1

        return clusters

    def _get_formatted_cluster(self, full_cluster):
        # logger.debug('_get_formatted_cluster called')
        formatted_cluster = {}

        for question in full_cluster:
            cluster_head_dic = {}
            for cluster_head in full_cluster[question]:
                head, avg, count = self._get_best_head_avg_count(full_cluster[question][cluster_head])
                # logger.debug('head:', head, 'avg:', avg, 'count:', count)
                cluster_elements = []
                for item in full_cluster[question][cluster_head]:
                    try:
                        sentence_cid = self.all_sents[item[1]]
                        sentence = sentence_cid[0]
                        comment = self.all_comments[sentence_cid[1]][0]
                        cluster_elements.append([item[0], sentence, comment])
                    except Exception as e:
                        # logger.error(str(e))
                        continue

                cluster_head_dic[head] = {'cluster_elements': cluster_elements, 'similarity_score': avg}

            formatted_cluster[question] = cluster_head_dic

        return formatted_cluster

    def create_clusters_from_queries(self, query_list, min_clusters, max_clusters, min_similarity_start):
        # logger.debug('create_clusters_from_queries called')
        full_cluster_all = {}
        query_dic = self._get_answers_from_queries(query_list)

        for q in query_dic:
            if len(query_dic[q]) > 0:
                answers = [item[0] for item in query_dic[q]]
                embeddings = [item[1][0] for item in query_dic[q]]
                ids = [item[2] for item in query_dic[q]]

                if len(query_dic[q]) > 20:
                    X = np.array(embeddings)
                    clustering = AgglomerativeClustering(n_clusters=max_clusters).fit(X)
                    labels = clustering.labels_
                else:
                    labels = [0 for i in range(len(query_dic[q]))]

                while True:
                    all_mini_clusters = self._get_best_clusters(
                        labels,
                        embeddings,
                        answers,
                        ids,
                        min_similarity_start
                    )
                    full_cluster_all[q] = {}

                    # logger.debug('len(all_mini_clusters):', str(len(all_mini_clusters)))
                    if len(all_mini_clusters) > 0:
                        all_mini_clusters_keys = list(all_mini_clusters.keys())
                        all_mini_cluster_embeddings = self.embedder.get_embeddings(all_mini_clusters_keys)
                        all_mini_clusters_ids = [all_mini_clusters[item][0][1] for item in all_mini_clusters]
                        clusters_from_keys = self._get_mini_clusters(
                            all_mini_cluster_embeddings,
                            all_mini_clusters_keys,
                            all_mini_clusters_ids,
                            min_similarity_start
                        )
                        full_cluster = {}
                        for item in clusters_from_keys:
                            full_cluster[item] = []
                            for item2 in clusters_from_keys[item]:
                                full_cluster[item].extend(all_mini_clusters[item2[0]])

                        full_cluster_all[q] = full_cluster

                    if len(full_cluster_all[q]) > min_clusters or min_similarity_start <= 0.3:
                        break
                    else:
                        min_similarity_start -= 0.1
                
                if len(full_cluster_all[q]) > max_clusters:
                    full_cluster_all[q] = self._merge_clusters(full_cluster_all[q], max_clusters)

        return self._get_formatted_cluster(full_cluster_all)
