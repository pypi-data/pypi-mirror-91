# Adapted from https://github.com/abalter/polyglottus/blob/master/simple_kernel.py

import queue
from jupyter_client.manager import start_new_kernel
from pprint import PrettyPrinter

POLL_TIME = 0.2

class SimpleKernel():
    """
    ## Description
    **SimpleKernel**:
     A simplistic Jupyter kernel client wrapper.
    Additional information in [this GitHub issue]
    (
    )
    """

    def __init__(self, kernel_name='python3'):
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

        ### Initialize pretty printer
        self.pp = PrettyPrinter(indent=2)

    ### end __init__ ####

    def executesilent(self, code, allow_errors=False):
        '''Do not collect output, but run the code, wait for it to finish and check for errors'''
        msg_id = self.client.execute(code)
        io_msg_content = self.client.get_iopub_msg(timeout=1)['content']

        ### We're going to catch this here before we start polling
        if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
            return True

        ### Continue polling for execution to complete
        ### which is indicated by having an execution state of "idle"
        while True:
            ### Check the message for various possibilities
            if 'traceback' in io_msg_content: # Indicates error
                if allow_errors:
                    return False
                else:
                    raise AttributeError
            ### Poll the message in intervals of length POLL_TIME seconds
            try:
                io_msg_content = self.client.get_iopub_msg(timeout=POLL_TIME)['content']
                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    break
            except queue.Empty:
                break
        return True

    def execute(self, code, verbose=False, allow_errors=False):
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
        debug = lambda x: print(x if verbose else '')

        debug("----------------")
        debug("executing code: " + code)

        ### Execute the code
        msg_id = self.client.execute(code)

        ### Collect the response payload
        reply = self.client.get_shell_msg(msg_id)
        debug("reply content")
        debug(reply['content'])

        ### Get the execution status
        ### When the execution state is "idle" it is complete
        io_msg_content = self.client.get_iopub_msg(timeout=1)['content']
        debug("io_msg content")
        debug(io_msg_content)

        out = []
        ### We're going to catch this here before we start polling
        if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
            return []

        ### Continue polling for execution to complete
        ### which is indicated by having an execution state of "idle"
        while True:
            ### Check the message for various possibilities
            if 'data' in io_msg_content: # Indicates completed operation
                debug('has data')
                out.append(io_msg_content['data'])
            elif 'name' in io_msg_content and io_msg_content['name'] == "stdout": # indicates output
                debug('name is stdout')
                out.append({'text/plain':io_msg_content['text']})
            elif 'traceback' in io_msg_content: # Indicates error
                debug("ERROR")
                debug('\n'.join(io_msg_content['traceback'])) # Put error into nice format
                if allow_errors:
                    out.append({'error': '\n'.join(io_msg_content['traceback'])})
                else:
                    raise AttributeError

            ### Poll the message
            try:
                io_msg_content = self.client.get_iopub_msg(timeout=1)['content']
                debug("io_msg content")
                debug(io_msg_content)
                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    break
            except queue.Empty:
                debug("timeout get_iopub_msg")
                break

        debug("----------------\n\n")
        debug("returning " + str(out))
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
