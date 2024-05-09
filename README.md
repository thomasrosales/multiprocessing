# Threading

## Queues

The queue module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming when information must be exchanged safely between multiple threads. The Queue class in this module implements all the required locking semantics [Documentation](https://docs.python.org/3/library/queue.html#queue.Queue).

## Thread

The Thread class represents an activity that is run in a separate thread of control. There are two ways to specify the activity: by passing a callable object to the constructor, or by overriding the run() method in a subclass. No other methods (except for the constructor) should be overridden in a subclass. In other words, only override the __init__() and run() methods of this class.

Once a thread object is created, its activity must be started by calling the thread’s start() method. This invokes the run() method in a separate thread of control.

Once the thread’s activity is started, the thread is considered ‘alive’. It stops being alive when its run() method terminates – either normally, or by raising an unhandled exception. The is_alive() method tests whether the thread is alive.

Other threads can call a thread’s join() method. This blocks the calling thread until the thread whose join() method is called is terminated.

A thread has a name. The name can be passed to the constructor, and read or changed through the name attribute [Documentation](https://docs.python.org/3/library/threading.html#thread-objects).

## Lock

A primitive lock is a synchronization primitive that is not owned by a particular thread when locked. In Python, it is currently the lowest level synchronization primitive available, implemented directly by the _thread extension module.

A primitive lock is in one of two states, “locked” or “unlocked”. It is created in the unlocked state. It has two basic methods, acquire() and release(). When the state is unlocked, acquire() changes the state to locked and returns immediately. When the state is locked, acquire() blocks until a call to release() in another thread changes it to unlocked, then the acquire() call resets it to locked and returns. The release() method should only be called in the locked state; it changes the state to unlocked and returns immediately. If an attempt is made to release an unlocked lock, a RuntimeError will be raised [Documentation](https://docs.python.org/3/library/threading.html#lock-objects).

Locks also support the context management protocol.


# Multiprocessing

multiprocessing is a package that supports spawning processes using an API similar to the threading module. The multiprocessing package offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads. Due to this, the multiprocessing module allows the programmer to fully leverage multiple processors on a given machine. It runs on both POSIX and Windows.

The multiprocessing module also introduces APIs which do not have analogs in the threading module. A prime example of this is the Pool object which offers a convenient means of parallelizing the execution of a function across multiple input values, distributing the input data across processes (data parallelism). The following example demonstrates the common practice of defining such functions in a module so that child processes can successfully import that module. This basic example of data parallelism using Pool.

[Documentation](https://docs.python.org/3/library/multiprocessing.html)


## Process

The multiprocessing package mostly replicates the API of the threading module.

Process objects represent activity that is run in a separate process. The Process class has equivalents of all the methods of threading.Thread [Documentation](https://docs.python.org/3/library/multiprocessing.html#process-and-exceptions).


# Asyncio

asyncio is a library to write concurrent code using the async/await syntax.

asyncio is used as a foundation for multiple Python asynchronous frameworks that provide high-performance network and web-servers, database connection libraries, distributed task queues, etc.

asyncio is often a perfect fit for IO-bound and high-level structured network code [Documentation](https://docs.python.org/es/3/library/asyncio.html).

# Resources

- [Validate YAML Python Schema](https://www.andrewvillazon.com/validate-yaml-python-schema/)
- [Schema](https://github.com/keleshev/schema)