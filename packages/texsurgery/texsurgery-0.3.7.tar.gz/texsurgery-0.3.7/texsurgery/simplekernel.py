# Adapted from https://github.com/abalter/polyglottus/blob/master/simple_kernel.py

import queue
from jupyter_client.manager import start_new_kernel

POLL_TIME = 0.01

class SimpleKernel():
    """
    ## Description
    **SimpleKernel**:
     A simplistic Jupyter kernel client wrapper.
    Additional information in [this GitHub issue]
    (
    )
    """

    def __init__(self, kernel_name='python3', timeout=1, verbose=False):
        """
        ## Description
        Initializes the `kernel_manager` and `client` objects
        and starts the kernel. Also initializes the pretty printer
        for displaying object properties and execution result
        payloads.
        ## Parameters
        None.
        """
        ### Initialize kernel and client
        self.kernel_manager, self.client = start_new_kernel(kernel_name=kernel_name)
        # A short POLL_TIME is used for executesilent, since we don't have to wait for
        #  the output, and execute, where we do have to wait, and if we don't, the result
        #  can not be trusted.
        self.timeout = timeout
        self.pending_jobs = 0
        # TODO: use logging module
        self.debug = lambda *args:print(*args) if verbose else lambda *args: None

    ### end __init__ ####

    def executesilent(self, code, allow_errors=False):
        '''Do not collect output, but run the code, wait for it to finish and check for errors'''
        self.debug("----------------")
        self.debug("executing code: " + code)
        msg_id = self.client.execute(code)
        self.pending_jobs += 1

        ### Continue polling for execution to complete
        ### which is indicated by having an execution state of "idle"
        while True:
            ### Poll the message in intervals of length POLL_TIME seconds
            try:
                io_msg_content = self.client.get_iopub_msg(timeout=POLL_TIME)['content']
                self.debug("io_msg content")
                self.debug(io_msg_content)
                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    self.pending_jobs -= 1
                    self.debug('pending job recovered', self.pending_jobs)
                    if self.pending_jobs==0:
                        return True
            except queue.Empty:
                self.debug('pending job', self.pending_jobs)
                return True

            ### Check the message for various possibilities
            if 'traceback' in io_msg_content: # Indicates error
                if allow_errors:
                    return False
                else:
                    raise AttributeError

    def execute(self, code, allow_errors=False):
        """
        ## Description
        **execute**:
        Executes a code string in the kernel. Can return either
        the full execution response payload, or just `stdout`. Also,
        there is a verbose mode that displays the execution process.
        ## Parameters
        code : string
            The code string to get passed to `stdin`.
        verbose : bool (default=False)
            Whether to display processing information.
        get_type : bool (default=False) NOT IMPLEMENTED
            When implemented, will return a dict including the output
            and the type. E.g.
            1+1 ==> {stdout: 2, type: int}
            "hello" ==> {stdout: "hello", type: str}
            print("hello") ==> {stdout: "hello", type: NoneType}
            a=10 ==> {stdout: None, type: None}
        ## Returns
        `stdout` or the full response payload.
        """
        self.debug("----------------")
        self.debug("executing code: " + code)

        ### Execute the code
        msg_id = self.client.execute(code)
        self.pending_jobs += 1

        ### Collect the response payload
        reply = self.client.get_shell_msg(msg_id)
        self.debug("reply content")
        self.debug(reply['content'])

        out = []

        ### Continue polling for execution to complete
        ### which is indicated by having an execution state of "idle"
        while True:
            ### Poll the message
            try:
                io_msg_content = self.client.get_iopub_msg(timeout=self.timeout)['content']
                self.debug("io_msg content")
                self.debug(io_msg_content)
                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    self.pending_jobs -= 1
                    self.debug('pending job recovered', self.pending_jobs)
                    if self.pending_jobs==0:
                        break
            except queue.Empty:
                self.debug("timeout get_iopub_msg")
                raise TimeoutError

            ### Check the message for various possibilities
            if 'data' in io_msg_content: # Indicates completed operation
                self.debug('has data')
                out.append(io_msg_content['data'])
            elif 'name' in io_msg_content and io_msg_content['name'] == "stdout": # indicates output
                self.debug('name is stdout')
                out.append({'text/plain':io_msg_content['text']})
            elif 'traceback' in io_msg_content: # Indicates error
                self.debug("ERROR")
                self.debug('\n'.join(io_msg_content['traceback'])) # Put error into nice format
                if allow_errors:
                    out.append({'error': '\n'.join(io_msg_content['traceback'])})
                else:
                    raise AttributeError

        self.debug("----------------\n\n")
        self.debug("returning " + str(out))
        return out

    ### end execute ####

    def __del__(self):
        """
        ## Description
        Destructor. Shuts down kernel safely.
        """
        from zmq.error import ZMQError
        try:
            self.kernel_manager.shutdown_kernel()
        except (ZMQError, AttributeError) as e:
            pass
