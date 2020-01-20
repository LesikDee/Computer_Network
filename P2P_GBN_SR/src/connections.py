import multiprocessing as mp
from queue import Empty
import time
from collections import deque
import array
import random
random.seed(20)

random.random()


class PointToPoint:
    _window_size: int
    _lose_prob: float

    _sender_queue: mp.Queue()
    _receiver_queue: mp.Queue()

    def __init__(self, protocol_type: str, window_size, lose_prob, transfer_number=-1, seconds=-1):
        self._lose_prob = lose_prob
        self._window_size = window_size

        self._sender_queue = mp.Queue()
        self._receiver_queue = mp.Queue()

        sender = {
            'sr': {
                'number': self._sr_sender_number,
                'time': self._sr_sender_time
            },
            'gbn': {
                'number': self._gbn_sender_number,
                'time': self._gbn_sender_time
            }
        }
        receiver ={
            'sr': self._sr_receiver,
            'gbn': self._gbn_receiver
        }

        if protocol_type != 'gbn' and protocol_type != 'sr':
            raise ValueError
#sender[protocol_type]['number'] self_queue: mp.Queue(), dist_queue: mp.Queue(), window_size, lose_prob
        if transfer_number > 0:
            self._sender_process = mp.Process(target=sender[protocol_type]['number'],
                                              args=(self._sender_queue, self._receiver_queue,
                                                    window_size, lose_prob, transfer_number))
        if seconds > 0:
            self._sender_process = mp.Process(target=sender[protocol_type]['time'],
                                              args=(self._sender_queue, self._receiver_queue,
                                                    window_size, lose_prob, seconds))
        if transfer_number > 0 or seconds > 0:
            self._receiver_process = mp.Process(target=receiver['sr'],
                                                args=(self._receiver_queue, self._sender_queue, window_size, lose_prob))
        else:
            raise ValueError

    def start_transmission(self):
        self._sender_process.start()
        self._receiver_process.start()

        self._sender_process.join()
        self._receiver_process.terminate()

    class SenderArgs:
        def __init__(self, window_size, lose_prob, Sb = 0):
            self.Sn = 0
            self.Sm = window_size
            self.window_size = window_size
            self.need_check = False
            self.lose_prob = lose_prob
            self.Sb = Sb

    @staticmethod
    def _sr_sender_number(sender_queue, receiver_queue, window_size, lose_prob, pack_number):
        args = PointToPoint.SenderArgs(window_size, lose_prob)
        check_deque = deque()
        while args.Sn <= pack_number:
            PointToPoint._sr_sender(sender_queue, receiver_queue, check_deque, args)

    @staticmethod
    def _sr_sender_time(sender_queue, receiver_queue, window_size, lose_prob, work_time):
        args = PointToPoint.SenderArgs(window_size, lose_prob)
        check_deque = deque()

        start_time = time.time()
        while time.time() < start_time + work_time:
            PointToPoint._sr_sender(sender_queue, receiver_queue, check_deque, args)

    @staticmethod
    def _sr_sender(self_queue, dist_queue, check_deque, args: SenderArgs):
        if args.need_check:
            if len(check_deque) == 0:
                args.need_check = False
                args.Sn = args.Sm
                args.Sm = args.Sm + args.window_size
                return

            next_ack_number = check_deque.popleft()
            try:
                curr_ack = int(self_queue.get(timeout=0.1).split(':')[1])
            except Empty:
                PointToPoint._send(dist_queue, str(next_ack_number), args.lose_prob)
                check_deque.append(next_ack_number)
            else:
                if curr_ack != next_ack_number:
                    try:
                        check_deque.remove(curr_ack)
                    except ValueError:
                        pass

                    PointToPoint._send(dist_queue, str(next_ack_number), args.lose_prob)
                    check_deque.append(next_ack_number)

        else:
            PointToPoint._send(dist_queue, str(args.Sn), args.lose_prob)
            check_deque.append(args.Sn)
            args.Sn += 1
            if args.Sn == args.Sm:
                args.need_check = True

    @staticmethod
    def _send(queue: mp.Queue(), message: str, lose_prob):
        if random.random() >= lose_prob:
            queue.put(message)

    @staticmethod
    def _sr_receiver(self_queue: mp.Queue(), dist_queue: mp.Queue(), window_size, lose_prob):
        window_i = 0
        Sb, Sm = 0, window_size
        buffer = array.array('i', window_size * [0])
        PointToPoint._arr_init(buffer)
        while True:
            message_number = self_queue.get()
            PointToPoint._send(dist_queue, 'ACK:' + message_number, lose_prob)
            number = int(message_number)
            buffer_ind = int(message_number) % window_size

            if buffer[buffer_ind] == -1 and Sb <= number < Sm:
                window_i += 1
                buffer[buffer_ind] = number

            if window_i == window_size:
                window_i = 0
                Sb, Sm = Sb + window_size, Sm + window_size
                PointToPoint.print_buffer(buffer)
                PointToPoint._arr_init(buffer)

    @staticmethod
    def _arr_init(buffer):
        for i in range(len(buffer)):
            buffer[i] = -1

    @staticmethod
    def print_buffer(buffer):
        for i in range(len(buffer)):
            print('receiver: ', str(buffer[i]))

    @staticmethod
    def _gbn_sender_number(sender_queue, receiver_queue, window_size, lose_prob, pack_number):
        args = PointToPoint.SenderArgs(window_size, lose_prob)
        while args.Sn <= pack_number:
            PointToPoint._gbn_sender(sender_queue, receiver_queue, args)

    @staticmethod
    def _gbn_sender_time(sender_queue, receiver_queue, window_size, lose_prob, work_time):
        args = PointToPoint.SenderArgs(window_size, lose_prob)

        start_time = time.time()
        while time.time() < start_time + work_time:
            PointToPoint._gbn_sender(sender_queue, receiver_queue, args)

    @staticmethod
    def _gbn_sender(self_queue: mp.Queue(), dist_queue: mp.Queue(), args: SenderArgs):
        repeat = False
        if args.Sn < args.Sm:
            PointToPoint._send(dist_queue, str(args.Sn), args.lose_prob)
            args.Sn += 1
        else:
            try:
                message_number = self_queue.get(timeout=0.1).split(':')[1]
                print('sender: ACK' + message_number)
                if int(message_number) == args.Sb:
                    PointToPoint._send(dist_queue, str(args.Sn), args.lose_prob)
                    args.Sn, args.Sb, args.Sm = args.Sn + 1, args.Sb + 1, args.Sm + 1
                else:
                    repeat = True
            except Empty:
                repeat = True

        if repeat:
            args.Sn = args.Sb

    @staticmethod
    def _gbn_receiver(self_queue: mp.Queue(), dist_queue: mp.Queue(), N: int, lose_prob):
        Rn = 0
        while True:
            message_number = self_queue.get()
            #print('receiver get ', message_number)

            if Rn == int(message_number):
                print('receiver recieved: ', message_number)
                PointToPoint._send(dist_queue, 'ACK:' + str(Rn), lose_prob)
                Rn += 1
            elif Rn < int(message_number):
                PointToPoint._send(dist_queue, 'ACK:' + str(Rn - 1), lose_prob)
            else:
                PointToPoint._send(dist_queue, 'ACK:' + message_number, lose_prob)


if __name__ == '__main__':
    wz = 4
    lb = 0.5
    conn = PointToPoint('gbn', wz, lb, seconds=2)
    conn.start_transmission()
