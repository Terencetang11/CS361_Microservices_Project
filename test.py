from multiprocessing import Process, Queue
from content_generator_microservice import CG

if __name__ == '__main__':

    q = Queue()
    # Life Generator sends data and appends it to Queue
    data = ['Portland','Oregon']
    q.put(data)

    # Set up Content Generator process
    p = Process(target=CG, args=(q,))

    # Content generator receives data, processes, appends result back in queue
    p.start()
    p.join()

    # Data is available in the queue for Life_Generator 
    print(q.get())