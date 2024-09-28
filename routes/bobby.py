import json
import logging
import heapq

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def max_bugsfixed(bugseq):

    bugseq.sort(key=lambda x: x[1])
    
    heap = []
    total_time = 0
    
    for difficulty, limit in bugseq:
        heapq.heappush(heap, difficulty)
        total_time += difficulty
        
        if total_time > limit:
            total_time -= heapq.heappop(heap)
    
    return len(heap)

@app.route('/bobby', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    for item in data:
        bugseq = item.get("bugseq")
        result = max_bugsfixed(bugseq)
        results.append(result)
    logging.info("My result :{}".format(results))
    return json.dumps(results)