# Asyncio Deep Dive: Mastering Asynchronous Python

!!! note "AI Assisted (Claude Sonnet 4)"

## The Fundamental Problem: Why Asyncio Exists

Traditional Python code executes **synchronously** - one operation at a time, waiting for each to complete before starting the next. This creates a critical inefficiency problem:

```python
import time
import requests

def sequential_downloads():
    """Traditional synchronous approach"""
    print("🐌 Starting sequential downloads...")
    start = time.time()
    
    # Each request blocks until complete
    response1 = requests.get("https://httpbin.org/delay/2")  # Wait 2 seconds
    print(f"✅ First download complete")
    
    response2 = requests.get("https://httpbin.org/delay/2")  # Wait another 2 seconds  
    print(f"✅ Second download complete")
    
    response3 = requests.get("https://httpbin.org/delay/2")  # Wait another 2 seconds
    print(f"✅ Third download complete")
    
    total_time = time.time() - start
    print(f"⏱️  Total time: {total_time:.2f} seconds")  # ~6 seconds
    
    return [response1, response2, response3]

# sequential_downloads()  # Uncomment to see the slow approach
```

**The inefficiency:** While waiting for the first request, your CPU sits idle even though it could be starting the second and third requests simultaneously.

**Asyncio's solution:** Enable **cooperative multitasking** where your program can juggle multiple operations, switching between them while waiting for I/O:

```python
import asyncio
import aiohttp
import time

async def concurrent_downloads():
    """Asyncio's concurrent approach"""
    print("🚀 Starting concurrent downloads...")
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Start all three requests simultaneously
        tasks = [
            session.get("https://httpbin.org/delay/2"),
            session.get("https://httpbin.org/delay/2"), 
            session.get("https://httpbin.org/delay/2")
        ]
        
        # Wait for all to complete
        responses = await asyncio.gather(*tasks)
        
        # Process responses
        for i, response in enumerate(responses, 1):
            print(f"✅ Download {i} complete")
            response.close()
    
    total_time = time.time() - start
    print(f"⏱️  Total time: {total_time:.2f} seconds")  # ~2 seconds!
    
    return responses

asyncio.run(concurrent_downloads())
```

**Key insight:** Asyncio doesn't make individual operations faster - it eliminates wasted waiting time by running operations concurrently.

## The Event Loop: The Heart of Asyncio

The **event loop** is asyncio's central coordinator - a single-threaded mechanism that manages and executes asynchronous tasks. Think of it as a highly efficient restaurant manager:

```python
import asyncio
import random
import time

async def restaurant_simulation():
    """Demonstrates how the event loop coordinates multiple operations"""
    
    async def serve_customer(customer_id, service_time):
        print(f"🍽️  Customer {customer_id}: Order taken")
        
        # This represents I/O waiting (kitchen preparing food)
        # The event loop can serve other customers during this time
        await asyncio.sleep(service_time)
        
        print(f"✅ Customer {customer_id}: Order ready! ({service_time}s)")
        return f"Meal for customer {customer_id}"
    
    print("🏪 Restaurant opens - Multiple customers arrive")
    
    # Customers with different service times
    customers = [
        serve_customer(1, 3.0),  # Slow order
        serve_customer(2, 1.0),  # Fast order
        serve_customer(3, 2.0),  # Medium order
        serve_customer(4, 1.5),  # Medium-fast order
    ]
    
    # Event loop serves all customers concurrently
    start_time = time.time()
    meals = await asyncio.gather(*customers)
    total_time = time.time() - start_time
    
    print(f"🏪 All customers served in {total_time:.1f}s")
    print("Notice: Faster orders completed first, regardless of arrival order!")
    
    return meals

asyncio.run(restaurant_simulation())
```

**Event Loop Mechanics:**

The event loop operates on a simple but powerful principle:

1. **Run ready tasks** until they hit an `await` (suspension point)
2. **Track waiting tasks** and when they'll be ready to resume
3. **Resume tasks** as their wait conditions are met
4. **Repeat** until all tasks complete

Here's a simplified view of what happens internally:

```python
# Conceptual view - don't run this code
class ConceptualEventLoop:
    def __init__(self):
        self.ready_tasks = []       # Tasks ready to run now
        self.waiting_tasks = []     # Tasks waiting for I/O or timers
        self.time_callbacks = []    # Scheduled callbacks
    
    def run_until_complete(self, main_task):
        """Main event loop execution"""
        self.ready_tasks.append(main_task)
        
        while self.ready_tasks or self.waiting_tasks:
            # Execute all ready tasks
            while self.ready_tasks:
                task = self.ready_tasks.pop(0)
                try:
                    # Run task until it hits 'await'
                    task.step()
                except TaskComplete:
                    continue  # Task finished
                except TaskSuspended as suspend_info:
                    # Task is waiting for something
                    self.waiting_tasks.append((task, suspend_info))
            
            # Check which waiting tasks are now ready
            self.check_waiting_tasks()
            
            # Handle timer callbacks
            self.handle_timer_callbacks()
    
    def check_waiting_tasks(self):
        """Move completed waits back to ready queue"""
        still_waiting = []
        for task, wait_info in self.waiting_tasks:
            if wait_info.is_ready():
                self.ready_tasks.append(task)
            else:
                still_waiting.append((task, wait_info))
        self.waiting_tasks = still_waiting
```

## Coroutines: The Building Blocks

**Coroutines** are special functions that can be suspended and resumed. They're the fundamental units of work in asyncio.

### Creating and Understanding Coroutines

```python
import asyncio

# Regular function - runs to completion immediately
def regular_function(name):
    print(f"Regular function {name} starting")
    return f"Result from {name}"

# Coroutine function - can be suspended and resumed
async def coroutine_function(name):
    print(f"Coroutine {name} starting")
    
    # This is a suspension point - execution can pause here
    await asyncio.sleep(1)
    
    print(f"Coroutine {name} resuming after 1 second")
    return f"Async result from {name}"

async def demonstrate_coroutine_lifecycle():
    print("=== Regular Function ===")
    result = regular_function("RegularFunc")
    print(f"Result: {result}")
    
    print("\n=== Coroutine Function ===")
    
    # Calling a coroutine function doesn't run it!
    coro = coroutine_function("CoroFunc")
    print(f"Coroutine object created: {type(coro)}")
    
    # You must await it to actually run it
    result = await coro
    print(f"Result: {result}")
    
    print("\n=== Multiple Coroutines Concurrently ===")
    # Multiple coroutines can run together
    results = await asyncio.gather(
        coroutine_function("Coro1"),
        coroutine_function("Coro2"), 
        coroutine_function("Coro3")
    )
    print(f"All results: {results}")

asyncio.run(demonstrate_coroutine_lifecycle())
```

### Coroutine States and Execution Flow

```python
import asyncio
import inspect

async def trace_coroutine_execution():
    """Demonstrates the different states a coroutine goes through"""
    
    async def traced_operation(operation_id):
        print(f"🚀 Operation {operation_id}: Starting")
        
        print(f"⏸️  Operation {operation_id}: About to suspend (await)")
        await asyncio.sleep(1)  # Suspension point
        
        print(f"▶️  Operation {operation_id}: Resumed after await")
        
        print(f"⏸️  Operation {operation_id}: Another suspension point")
        await asyncio.sleep(0.5)
        
        print(f"✅ Operation {operation_id}: Completed")
        return f"Result-{operation_id}"
    
    print("Creating coroutines (not running yet)...")
    coro1 = traced_operation("A")
    coro2 = traced_operation("B")
    
    print(f"Coroutine states: {inspect.getcoroutinestate(coro1)}")
    
    print("\nStarting concurrent execution...")
    results = await asyncio.gather(coro1, coro2)
    
    print(f"\nFinal results: {results}")

asyncio.run(trace_coroutine_execution())
```

## Understanding await: The Suspension Mechanism

The `await` keyword is where the magic happens. It's not just syntax - it's the mechanism that allows cooperative multitasking.

### What await Actually Does

```python
import asyncio
import time

async def demonstrate_await_behavior():
    """Shows exactly what happens at await points"""
    
    print("🎬 Starting demonstration")
    
    print("📍 Point 1: Before first await")
    start_time = time.time()
    
    # This suspends the coroutine and yields control to the event loop
    await asyncio.sleep(1)  
    
    print(f"📍 Point 2: After first await ({time.time() - start_time:.1f}s elapsed)")
    
    # Another suspension point
    await asyncio.sleep(0.5)
    
    print(f"📍 Point 3: After second await ({time.time() - start_time:.1f}s elapsed)")
    
    return "Demo complete"

async def demonstrate_concurrent_awaits():
    """Shows how multiple awaits can run concurrently"""
    
    async def worker(worker_id, work_duration):
        print(f"👷 Worker {worker_id}: Starting work ({work_duration}s)")
        await asyncio.sleep(work_duration)
        print(f"✅ Worker {worker_id}: Work complete")
        return f"Work result from {worker_id}"
    
    print("🏭 Starting workers concurrently...")
    start_time = time.time()
    
    # All workers start at the same time
    results = await asyncio.gather(
        worker("Alpha", 2.0),
        worker("Beta", 1.0),
        worker("Gamma", 1.5)
    )
    
    total_time = time.time() - start_time
    print(f"🏁 All work completed in {total_time:.1f}s")
    print(f"📊 Results: {results}")

async def main():
    await demonstrate_await_behavior()
    print("\n" + "="*50 + "\n")
    await demonstrate_concurrent_awaits()

asyncio.run(main())
```

### await Rules and Awaitables

Not everything can be awaited. Only **awaitable** objects work with `await`:

```python
import asyncio

class CustomAwaitable:
    """Example of creating a custom awaitable object"""
    
    def __init__(self, value, delay):
        self.value = value
        self.delay = delay
    
    def __await__(self):
        """This makes the object awaitable"""
        # Yield control to event loop for the specified delay
        yield from asyncio.sleep(self.delay).__await__()
        # Return the final value
        return f"Custom result: {self.value}"

async def demonstrate_awaitables():
    print("=== Built-in Awaitables ===")
    
    # Coroutines are awaitable
    async def simple_coro():
        await asyncio.sleep(0.1)
        return "Coroutine result"
    
    result1 = await simple_coro()
    print(f"Coroutine result: {result1}")
    
    # Tasks are awaitable
    task = asyncio.create_task(simple_coro())
    result2 = await task
    print(f"Task result: {result2}")
    
    # Futures are awaitable
    future = asyncio.Future()
    future.set_result("Future result")
    result3 = await future
    print(f"Future result: {result3}")
    
    print("\n=== Custom Awaitable ===")
    custom = CustomAwaitable("Hello World", 0.5)
    result4 = await custom
    print(f"Custom awaitable result: {result4}")
    
    print("\n=== What's NOT Awaitable ===")
    try:
        # This will fail - regular functions aren't awaitable
        # await time.sleep(1)  # ❌ TypeError
        pass
    except TypeError as e:
        print(f"Error: {e}")

asyncio.run(demonstrate_awaitables())
```

## Tasks: Concurrent Execution Units

**Tasks** are the primary mechanism for running coroutines concurrently. They wrap coroutines and manage their execution within the event loop.

### Understanding Tasks vs Coroutines

```python
import asyncio
import time

async def demonstrate_tasks_vs_coroutines():
    """Shows the critical difference between creating coroutines and tasks"""
    
    async def background_work(work_id, duration):
        print(f"🔧 Work {work_id}: Starting ({duration}s)")
        for i in range(int(duration)):
            await asyncio.sleep(1)
            print(f"⚙️  Work {work_id}: Progress {i+1}/{int(duration)}")
        print(f"✅ Work {work_id}: Complete")
        return f"Result-{work_id}"
    
    print("=== Coroutines: Don't Start Until Awaited ===")
    start_time = time.time()
    
    # Creating coroutines doesn't start them
    coro1 = background_work("Coro-A", 2)
    coro2 = background_work("Coro-B", 2)
    
    print(f"⏱️  Coroutines created at {time.time() - start_time:.1f}s")
    await asyncio.sleep(1)  # Wait 1 second
    print(f"⏱️  1 second later - no work has started yet")
    
    # Now run them sequentially
    result1 = await coro1  # Runs for 2 seconds
    result2 = await coro2  # Runs for another 2 seconds
    
    coro_time = time.time() - start_time
    print(f"⏱️  Coroutines completed in {coro_time:.1f}s (sequential)")
    
    print("\n=== Tasks: Start Immediately ===")
    start_time = time.time()
    
    # Creating tasks starts them immediately!
    task1 = asyncio.create_task(background_work("Task-A", 2))
    task2 = asyncio.create_task(background_work("Task-B", 2))
    
    print(f"⏱️  Tasks created at {time.time() - start_time:.1f}s")
    await asyncio.sleep(1)  # Wait 1 second
    print(f"⏱️  1 second later - work is already running!")
    
    # Wait for both to complete (they run concurrently)
    results = await asyncio.gather(task1, task2)
    
    task_time = time.time() - start_time
    print(f"⏱️  Tasks completed in {task_time:.1f}s (concurrent)")
    
    print(f"\n📊 Time difference: {coro_time - task_time:.1f}s saved with tasks!")

asyncio.run(demonstrate_tasks_vs_coroutines())
```

### Task Management and Control

```python
import asyncio
import random

async def demonstrate_task_management():
    """Shows how to manage, monitor, and control tasks"""
    
    async def worker_task(worker_id):
        """A worker that does some work and might fail"""
        try:
            work_time = random.uniform(1, 4)
            print(f"👷 Worker {worker_id}: Starting {work_time:.1f}s of work")
            
            # Simulate work with progress updates
            for i in range(int(work_time)):
                await asyncio.sleep(1)
                print(f"⚙️  Worker {worker_id}: {i+1}/{int(work_time)} seconds complete")
            
            # Simulate random failures
            if random.random() < 0.3:  # 30% chance of failure
                raise Exception(f"Worker {worker_id} encountered an error!")
            
            print(f"✅ Worker {worker_id}: Work completed successfully")
            return f"Success-{worker_id}"
            
        except asyncio.CancelledError:
            print(f"🛑 Worker {worker_id}: Cancelled during work")
            raise  # Re-raise to complete cancellation
    
    print("🏭 Starting worker management demo")
    
    # Create multiple tasks
    tasks = [
        asyncio.create_task(worker_task(f"W{i}"))
        for i in range(1, 6)
    ]
    
    # Monitor task progress
    async def monitor_tasks():
        while True:
            await asyncio.sleep(0.5)
            
            pending = [t for t in tasks if not t.done()]
            completed = [t for t in tasks if t.done() and not t.cancelled()]
            cancelled = [t for t in tasks if t.cancelled()]
            failed = [t for t in tasks if t.done() and t.exception()]
            
            print(f"📊 Status: {len(pending)} pending, {len(completed)} completed, "
                  f"{len(cancelled)} cancelled, {len(failed)} failed")
            
            if not pending:
                break
    
    monitor_task = asyncio.create_task(monitor_tasks())
    
    try:
        # Let tasks run for a bit
        await asyncio.sleep(2)
        
        # Cancel any remaining tasks that are taking too long
        for task in tasks:
            if not task.done():
                print(f"⏰ Cancelling slow task...")
                task.cancel()
        
        # Wait for all tasks to finish (including cancellation)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print("\n📋 Final Results:")
        for i, result in enumerate(results):
            if isinstance(result, asyncio.CancelledError):
                print(f"  Task {i+1}: Cancelled")
            elif isinstance(result, Exception):
                print(f"  Task {i+1}: Failed - {result}")
            else:
                print(f"  Task {i+1}: {result}")
                
    finally:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass

asyncio.run(demonstrate_task_management())
```

## Concurrent Execution Patterns

Asyncio provides several patterns for running multiple operations. Each has different use cases and behaviors.

### asyncio.gather(): All or Nothing Coordination

```python
import asyncio
import aiohttp
import time

async def fetch_url(session, url, name):
    """Fetch a URL and return info about the request"""
    start_time = time.time()
    print(f"🌐 {name}: Starting request to {url}")
    
    try:
        async with session.get(url) as response:
            content = await response.text()
            duration = time.time() - start_time
            
        print(f"✅ {name}: Completed in {duration:.2f}s ({len(content)} chars)")
        return {
            "name": name,
            "url": url,
            "duration": duration,
            "size": len(content),
            "status": response.status
        }
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ {name}: Failed after {duration:.2f}s - {e}")
        raise

async def demonstrate_gather():
    """Shows gather() behavior with success and failure scenarios"""
    
    print("=== gather() with all successful requests ===")
    async with aiohttp.ClientSession() as session:
        try:
            results = await asyncio.gather(
                fetch_url(session, "https://httpbin.org/delay/1", "Fast"),
                fetch_url(session, "https://httpbin.org/delay/2", "Medium"),
                fetch_url(session, "https://httpbin.org/delay/1.5", "Quick")
            )
            
            print("📊 All requests successful:")
            for result in results:
                print(f"  {result['name']}: {result['duration']:.2f}s")
                
        except Exception as e:
            print(f"❌ gather() failed: {e}")
    
    print("\n=== gather() with one failure (default behavior) ===")
    async with aiohttp.ClientSession() as session:
        try:
            results = await asyncio.gather(
                fetch_url(session, "https://httpbin.org/delay/1", "Success1"),
                fetch_url(session, "https://httpbin.org/status/500", "Failure"),  # Will fail
                fetch_url(session, "https://httpbin.org/delay/1", "Success2")
            )
        except Exception as e:
            print(f"❌ gather() failed fast due to: {e}")
    
    print("\n=== gather() with return_exceptions=True ===")
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            fetch_url(session, "https://httpbin.org/delay/1", "Success1"),
            fetch_url(session, "https://httpbin.org/status/500", "Failure"),
            fetch_url(session, "https://httpbin.org/delay/1", "Success2"),
            return_exceptions=True  # Don't fail, return exceptions
        )
        
        print("📊 Mixed results (exceptions returned):")
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"  Request {i+1}: Failed - {result}")
            else:
                print(f"  Request {i+1}: Success - {result['name']}")

asyncio.run(demonstrate_gather())
```

### asyncio.as_completed(): Process Results as They Arrive

```python
import asyncio
import random
import time

async def variable_duration_task(task_id):
    """Task with random duration to demonstrate as_completed behavior"""
    duration = random.uniform(0.5, 3.0)
    print(f"🚀 Task {task_id}: Starting ({duration:.1f}s estimated)")
    
    await asyncio.sleep(duration)
    
    print(f"✅ Task {task_id}: Completed after {duration:.1f}s")
    return {
        "task_id": task_id,
        "duration": duration,
        "completed_at": time.time()
    }

async def demonstrate_as_completed():
    """Shows how as_completed processes results in completion order"""
    
    print("🎯 Creating tasks with random durations")
    start_time = time.time()
    
    # Create tasks with different expected completion times
    tasks = [
        variable_duration_task(f"T{i}")
        for i in range(1, 6)
    ]
    
    print("⏳ Processing results as they complete (not in creation order):")
    
    completion_order = []
    
    # Process results as they become available
    for completed_task in asyncio.as_completed(tasks):
        result = await completed_task
        elapsed = time.time() - start_time
        
        completion_order.append(result['task_id'])
        print(f"📥 Received result from {result['task_id']} "
              f"after {elapsed:.1f}s total elapsed")
    
    total_time = time.time() - start_time
    print(f"\n📊 All tasks completed in {total_time:.1f}s")
    print(f"🔄 Completion order: {' → '.join(completion_order)}")
    print("💡 Notice: Results arrived in completion order, not creation order!")

async def demonstrate_as_completed_with_timeout():
    """Shows as_completed with timeout handling"""
    
    async def slow_task(task_id, duration):
        await asyncio.sleep(duration)
        return f"Task {task_id} result"
    
    print("\n" + "="*50)
    print("⏰ as_completed with timeout demonstration")
    
    tasks = [
        slow_task("A", 1),
        slow_task("B", 3),  # Will timeout
        slow_task("C", 2),
        slow_task("D", 4),  # Will timeout
    ]
    
    completed_count = 0
    timeout_seconds = 2.5
    
    try:
        for completed_task in asyncio.as_completed(tasks, timeout=timeout_seconds):
            try:
                result = await completed_task
                completed_count += 1
                print(f"✅ Completed {completed_count}: {result}")
            except asyncio.TimeoutError:
                print(f"⏰ Task timed out after {timeout_seconds}s")
                break
    except asyncio.TimeoutError:
        print(f"⏰ Overall timeout reached after {timeout_seconds}s")
        print(f"📊 Completed {completed_count} tasks before timeout")

async def main():
    await demonstrate_as_completed()
    await demonstrate_as_completed_with_timeout()

asyncio.run(main())
```

### asyncio.wait(): Fine-Grained Control

```python
import asyncio
import time

async def controlled_task(task_id, duration, should_fail=False):
    """Task for demonstrating wait() control features"""
    print(f"🚀 Task {task_id}: Starting")
    
    try:
        await asyncio.sleep(duration)
        
        if should_fail:
            raise ValueError(f"Task {task_id} intentionally failed")
        
        print(f"✅ Task {task_id}: Completed successfully")
        return f"Result from task {task_id}"
        
    except asyncio.CancelledError:
        print(f"🛑 Task {task_id}: Cancelled")
        raise

async def demonstrate_wait_conditions():
    """Shows different wait conditions and their behaviors"""
    
    print("=== FIRST_COMPLETED: Return when any task finishes ===")
    tasks = [
        asyncio.create_task(controlled_task("A", 1)),
        asyncio.create_task(controlled_task("B", 2)),
        asyncio.create_task(controlled_task("C", 3)),
    ]
    
    start_time = time.time()
    done, pending = await asyncio.wait(
        tasks, 
        return_when=asyncio.FIRST_COMPLETED
    )
    elapsed = time.time() - start_time
    
    print(f"⏱️  First completion after {elapsed:.1f}s")
    print(f"📊 {len(done)} completed, {len(pending)} still running")
    
    # Get result from completed task
    for task in done:
        result = await task
        print(f"🎯 First result: {result}")
    
    # Cancel remaining tasks
    for task in pending:
        task.cancel()
    
    # Wait for cancellation to complete
    await asyncio.wait(pending)
    
    print("\n=== FIRST_EXCEPTION: Return when any task fails ===")
    tasks = [
        asyncio.create_task(controlled_task("X", 2, should_fail=False)),
        asyncio.create_task(controlled_task("Y", 1, should_fail=True)),   # Will fail
        asyncio.create_task(controlled_task("Z", 3, should_fail=False)),
    ]
    
    start_time = time.time()
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_EXCEPTION
    )
    elapsed = time.time() - start_time
    
    print(f"⏱️  First exception after {elapsed:.1f}s")
    
    # Check for exceptions
    for task in done:
        try:
            result = await task
            print(f"✅ Task completed: {result}")
        except Exception as e:
            print(f"❌ Task failed: {e}")
    
    # Cancel and wait for remaining tasks
    for task in pending:
        task.cancel()
    await asyncio.wait(pending)

async def demonstrate_wait_with_timeout():
    """Shows wait() with timeout functionality"""
    
    print("\n=== wait() with timeout ===")
    tasks = [
        asyncio.create_task(controlled_task("Fast", 1)),
        asyncio.create_task(controlled_task("Medium", 3)),
        asyncio.create_task(controlled_task("Slow", 5)),
    ]
    
    start_time = time.time()
    
    # Wait up to 2 seconds
    done, pending = await asyncio.wait(
        tasks,
        timeout=2.0,
        return_when=asyncio.ALL_COMPLETED
    )
    
    elapsed = time.time() - start_time
    print(f"⏱️  Timeout reached after {elapsed:.1f}s")
    print(f"📊 {len(done)} completed, {len(pending)} timed out")
    
    # Process completed tasks
    for task in done:
        result = await task
        print(f"✅ Completed before timeout: {result}")
    
    # Handle timed-out tasks
    for task in pending:
        print(f"⏰ Task timed out, cancelling...")
        task.cancel()
    
    # Wait for cancellation
    await asyncio.wait(pending)

async def main():
    await demonstrate_wait_conditions()
    await demonstrate_wait_with_timeout()

asyncio.run(main())
```

## Synchronization: Coordinating Concurrent Operations

When multiple coroutines work with shared resources, you need synchronization primitives to prevent race conditions and coordinate access.

### asyncio.Lock: Mutual Exclusion

```python
import asyncio
import random

class SharedCounter:
    """Demonstrates the need for locks in concurrent operations"""
    
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()
        self.operation_log = []
    
    async def unsafe_increment(self, worker_id):
        """Unsafe increment that can cause race conditions"""
        # Read current value
        old_value = self.value
        
        # Simulate some processing time (this is where race conditions occur)
        await asyncio.sleep(0.01)
        
        # Write back the incremented value
        self.value = old_value + 1
        
        self.operation_log.append(f"Worker {worker_id}: {old_value} → {self.value}")
    
    async def safe_increment(self, worker_id):
        """Safe increment using a lock"""
        async with self.lock:  # Only one worker can execute this block at a time
            old_value = self.value
            
            # Even with delay, no race condition occurs
            await asyncio.sleep(0.01)
            
            self.value = old_value + 1
            self.operation_log.append(f"Worker {worker_id}: {old_value} → {self.value}")

async def demonstrate_race_conditions():
    """Shows the difference between safe and unsafe concurrent operations"""
    
    print("=== Race Condition Demonstration ===")
    
    # Test unsafe operations
    unsafe_counter = SharedCounter()
    
    print("🚨 Running UNSAFE concurrent increments...")
    tasks = [
        unsafe_counter.unsafe_increment(f"U{i}")
        for i in range(10)
    ]
    
    await asyncio.gather(*tasks)
    
    print(f"❌ Expected final value: 10, Actual: {unsafe_counter.value}")
    print("📋 Last few operations:")
    for log_entry in unsafe_counter.operation_log[-5:]:
        print(f"  {log_entry}")
    
    # Test safe operations
    safe_counter = SharedCounter()
    
    print("\n✅ Running SAFE concurrent increments...")
    tasks = [
        safe_counter.safe_increment(f"S{i}")
        for i in range(10)
    ]
    
    await asyncio.gather(*tasks)
    
    print(f"✅ Expected final value: 10, Actual: {safe_counter.value}")
    print("📋 Last few operations:")
    for log_entry in safe_counter.operation_log[-5:]:
        print(f"  {log_entry}")

async def demonstrate_lock_usage_patterns():
    """Shows different patterns for using locks effectively"""
    
    lock = asyncio.Lock()
    shared_resource = {"data": [], "processing_count": 0}
    
    async def producer(producer_id):
        """Produces data items"""
        for i in range(3):
            item = f"P{producer_id}-Item{i}"
            
            async with lock:
                shared_resource["data"].append(item)
                print(f"📦 Producer {producer_id} added: {item}")
            
            await asyncio.sleep(0.1)  # Simulate work between productions
    
    async def processor():
        """Processes data items"""
        processed_items = []
        
        while len(processed_items) < 9:  # Expect 3 producers × 3 items each
            async with lock:
                if shared_resource["data"]:
                    item = shared_resource["data"].pop(0)
                    shared_resource["processing_count"] += 1
                    current_count = shared_resource["processing_count"]
                else:
                    item = None
            
            if item:
                # Process outside the lock to allow other operations
                await asyncio.sleep(0.05)  # Simulate processing time
                processed_items.append(item)
                print(f"🔧 Processed: {item} (#{current_count})")
            else:
                # No items available, wait a bit
                await asyncio.sleep(0.01)
        
        return processed_items
    
    print("\n=== Producer-Consumer with Lock ===")
    
    # Start producers and processor concurrently
    producer_tasks = [producer(i) for i in range(1, 4)]
    processor_task = processor()
    
    results = await asyncio.gather(*producer_tasks, processor_task)
    processed_items = results[-1]  # Last result is from processor
    
    print(f"📊 Processing complete: {len(processed_items)} items processed")

async def main():
    await demonstrate_race_conditions()
    await demonstrate_lock_usage_patterns()

asyncio.run(main())
```

### asyncio.Semaphore: Limiting Concurrent Access

```python
import asyncio
import aiohttp
import time

class RateLimitedDownloader:
    """Demonstrates semaphore usage for controlling concurrent operations"""
    
    def __init__(self, max_concurrent_downloads=3):
        self.semaphore = asyncio.Semaphore(max_concurrent_downloads)
        self.download_stats = {
            "started": 0,
            "completed": 0,
            "failed": 0,
            "concurrent_peak": 0,
            "currently_running": 0
        }
        self.stats_lock = asyncio.Lock()
    
    async def download_file(self, session, url, file_id):
        """Download a file with concurrency limiting"""
        
        # Wait for permission to start download
        async with self.semaphore:
            # Update stats
            async with self.stats_lock:
                self.download_stats["started"] += 1
                self.download_stats["currently_running"] += 1
                if self.download_stats["currently_running"] > self.download_stats["concurrent_peak"]:
                    self.download_stats["concurrent_peak"] = self.download_stats["currently_running"]
            
            print(f"🌐 Download {file_id}: Starting (concurrent: {self.download_stats['currently_running']})")
            
            try:
                # Simulate download
                start_time = time.time()
                async with session.get(url) as response:
                    data = await response.read()
                    download_time = time.time() - start_time
                
                # Simulate file processing
                await asyncio.sleep(0.1)
                
                async with self.stats_lock:
                    self.download_stats["completed"] += 1
                    self.download_stats["currently_running"] -= 1
                
                print(f"✅ Download {file_id}: Complete ({len(data)} bytes in {download_time:.2f}s)")
                return {"file_id": file_id, "size": len(data), "duration": download_time}
                
            except Exception as e:
                async with self.stats_lock:
                    self.download_stats["failed"] += 1
                    self.download_stats["currently_running"] -= 1
                
                print(f"❌ Download {file_id}: Failed - {e}")
                raise

async def demonstrate_semaphore_benefits():
    """Shows how semaphores prevent overwhelming services"""
    
    print("=== Semaphore: Controlling Concurrent Downloads ===")
    
    # Create downloader with limit of 3 concurrent downloads
    downloader = RateLimitedDownloader(max_concurrent_downloads=3)
    
    # Prepare many download URLs
    urls = [f"https://httpbin.org/bytes/1024" for _ in range(10)]
    
    async with aiohttp.ClientSession() as session:
        # Start all downloads (but semaphore limits concurrency)
        download_tasks = [
            downloader.download_file(session, url, f"File-{i+1}")
            for i, url in enumerate(urls)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*download_tasks, return_exceptions=True)
        total_time = time.time() - start_time
    
    # Analyze results
    successful = [r for r in results if isinstance(r, dict)]
    failed = [r for r in results if isinstance(r, Exception)]
    
    print(f"\n📊 Download Statistics:")
    print(f"  Total downloads: {len(urls)}")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Peak concurrent: {downloader.download_stats['concurrent_peak']}")
    print(f"  Average time per download: {total_time/len(successful):.2f}s")

async def demonstrate_semaphore_vs_unlimited():
    """Compares semaphore-limited vs unlimited concurrent access"""
    
    async def unlimited_downloads():
        """Downloads without any concurrency limiting"""
        async def simple_download(session, url, file_id):
            start_time = time.time()
            async with session.get(url) as response:
                data = await response.read()
            duration = time.time() - start_time
            print(f"🚀 Unlimited {file_id}: {duration:.2f}s")
            return duration
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                simple_download(session, f"https://httpbin.org/delay/1", f"U{i}")
                for i in range(8)
            ]
            return await asyncio.gather(*tasks)
    
    async def limited_downloads():
        """Downloads with semaphore limiting to 3 concurrent"""
        semaphore = asyncio.Semaphore(3)
        
        async def limited_download(session, url, file_id):
            async with semaphore:
                start_time = time.time()
                async with session.get(url) as response:
                    data = await response.read()
                duration = time.time() - start_time
                print(f"🎛️  Limited {file_id}: {duration:.2f}s")
                return duration
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                limited_download(session, f"https://httpbin.org/delay/1", f"L{i}")
                for i in range(8)
            ]
            return await asyncio.gather(*tasks)
    
    print("\n" + "="*50)
    print("⚡ Unlimited Concurrent Downloads (may overwhelm server):")
    start_time = time.time()
    unlimited_results = await unlimited_downloads()
    unlimited_time = time.time() - start_time
    
    print(f"🎛️  Limited Concurrent Downloads (3 at a time):")
    start_time = time.time()
    limited_results = await limited_downloads()
    limited_time = time.time() - start_time
    
    print(f"\n📈 Comparison:")
    print(f"  Unlimited: {unlimited_time:.2f}s total, avg {sum(unlimited_results)/len(unlimited_results):.2f}s per download")
    print(f"  Limited:   {limited_time:.2f}s total, avg {sum(limited_results)/len(limited_results):.2f}s per download")

async def main():
    await demonstrate_semaphore_benefits()
    await demonstrate_semaphore_vs_unlimited()

asyncio.run(main())
```

### asyncio.Event: Signaling and Coordination

```python
import asyncio
import random
import time

async def demonstrate_event_coordination():
    """Shows how events coordinate multiple coroutines"""
    
    # Events for coordination
    start_event = asyncio.Event()
    data_ready_event = asyncio.Event()
    processing_complete_event = asyncio.Event()
    
    # Shared data
    shared_data = {"items": [], "processed_items": []}
    
    async def data_producer():
        """Produces data and signals when ready"""
        print("📦 Producer: Waiting for start signal...")
        await start_event.wait()
        
        print("📦 Producer: Starting data generation...")
        for i in range(5):
            item = f"Data-{i}"
            shared_data["items"].append(item)
            print(f"📦 Producer: Generated {item}")
            await asyncio.sleep(0.2)  # Simulate generation time
        
        print("📦 Producer: All data generated, signaling data_ready")
        data_ready_event.set()
    
    async def data_processor(processor_id):
        """Processes data after it's ready"""
        print(f"🔧 Processor {processor_id}: Waiting for data...")
        await data_ready_event.wait()
        
        print(f"🔧 Processor {processor_id}: Data is ready, starting processing...")
        
        while shared_data["items"]:
            if shared_data["items"]:  # Double-check in case another processor took it
                item = shared_data["items"].pop(0)
                
                # Simulate processing
                processing_time = random.uniform(0.1, 0.3)
                await asyncio.sleep(processing_time)
                
                processed_item = f"Processed-{item}-by-P{processor_id}"
                shared_data["processed_items"].append(processed_item)
                print(f"🔧 Processor {processor_id}: Completed {processed_item}")
        
        print(f"🔧 Processor {processor_id}: No more items to process")
        
        # Check if all processing is done
        if not shared_data["items"] and len(shared_data["processed_items"]) == 5:
            print(f"🔧 Processor {processor_id}: All processing complete, signaling completion")
            processing_complete_event.set()
    
    async def coordinator():
        """Coordinates the entire process"""
        print("👨‍💼 Coordinator: Setting up workers...")
        
        # Start producer and processors
        producer_task = asyncio.create_task(data_producer())
        processor_tasks = [
            asyncio.create_task(data_processor(i))
            for i in range(1, 4)  # 3 processors
        ]
        
        await asyncio.sleep(0.5)  # Let everyone get ready
        
        print("👨‍💼 Coordinator: Sending start signal!")
        start_event.set()
        
        # Wait for processing to complete
        await processing_complete_event.wait()
        
        print("👨‍💼 Coordinator: All work completed!")
        
        # Wait for all tasks to finish
        await producer_task
        await asyncio.gather(*processor_tasks)
        
        return shared_data["processed_items"]
    
    print("=== Event-Coordinated Processing Pipeline ===")
    results = await coordinator()
    print(f"📊 Final results: {len(results)} items processed")
    for item in results:
        print(f"  ✅ {item}")

async def demonstrate_event_patterns():
    """Shows common event usage patterns"""
    
    async def waiter(waiter_id, event):
        """Waits for an event with timeout"""
        print(f"⏳ Waiter {waiter_id}: Waiting for event...")
        
        try:
            await asyncio.wait_for(event.wait(), timeout=2.0)
            print(f"🎉 Waiter {waiter_id}: Event received!")
        except asyncio.TimeoutError:
            print(f"⏰ Waiter {waiter_id}: Timeout waiting for event")
    
    async def delayed_setter(event, delay, event_name):
        """Sets an event after a delay"""
        print(f"⏰ Setter: Will signal '{event_name}' in {delay}s")
        await asyncio.sleep(delay)
        print(f"📢 Setter: Signaling '{event_name}'!")
        event.set()
    
    print("\n=== Event Timeout Patterns ===")
    
    # Test 1: Event set before timeout
    quick_event = asyncio.Event()
    await asyncio.gather(
        waiter("A", quick_event),
        delayed_setter(quick_event, 1.0, "quick_event")
    )
    
    # Test 2: Event not set before timeout
    slow_event = asyncio.Event()
    await asyncio.gather(
        waiter("B", slow_event),
        delayed_setter(slow_event, 3.0, "slow_event")  # Will timeout
    )

async def main():
    await demonstrate_event_coordination()
    await demonstrate_event_patterns()

asyncio.run(main())
```

## Error Handling and Resilience

Proper error handling in asyncio requires understanding how exceptions propagate through concurrent operations.

### Exception Propagation in Concurrent Code

```python
import asyncio
import random

async def demonstrate_exception_propagation():
    """Shows how exceptions behave in different asyncio patterns"""
    
    async def reliable_task(task_id):
        await asyncio.sleep(0.5)
        return f"Success from {task_id}"
    
    async def unreliable_task(task_id, failure_rate=0.5):
        await asyncio.sleep(0.5)
        if random.random() < failure_rate:
            raise ValueError(f"Task {task_id} failed randomly!")
        return f"Success from {task_id}"
    
    print("=== gather() Exception Behavior ===")
    
    print("🧪 Test 1: gather() with default behavior (fail fast)")
    try:
        results = await asyncio.gather(
            reliable_task("R1"),
            unreliable_task("U1", failure_rate=1.0),  # Will definitely fail
            reliable_task("R2")
        )
        print(f"✅ All completed: {results}")
    except Exception as e:
        print(f"❌ gather() failed: {e}")
        print("💡 Note: When one task fails, gather() raises immediately")
    
    print("\n🧪 Test 2: gather() with return_exceptions=True")
    results = await asyncio.gather(
        reliable_task("R3"),
        unreliable_task("U2", failure_rate=1.0),  # Will definitely fail
        reliable_task("R4"),
        return_exceptions=True  # Return exceptions instead of raising
    )
    
    print("📊 Mixed results:")
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  Task {i+1}: ❌ {result}")
        else:
            print(f"  Task {i+1}: ✅ {result}")

async def demonstrate_task_exception_handling():
    """Shows proper exception handling with individual tasks"""
    
    async def monitored_task(task_id, should_fail=False):
        try:
            await asyncio.sleep(0.3)
            if should_fail:
                raise RuntimeError(f"Task {task_id} encountered an error")
            return f"Result from {task_id}"
        except asyncio.CancelledError:
            print(f"🛑 Task {task_id}: Cancelled")
            raise  # Always re-raise CancelledError
    
    print("\n=== Individual Task Exception Handling ===")
    
    # Create tasks
    tasks = [
        asyncio.create_task(monitored_task("T1", should_fail=False)),
        asyncio.create_task(monitored_task("T2", should_fail=True)),
        asyncio.create_task(monitored_task("T3", should_fail=False)),
        asyncio.create_task(monitored_task("T4", should_fail=True)),
    ]
    
    # Handle each task individually
    results = []
    for i, task in enumerate(tasks):
        try:
            result = await task
            results.append(result)
            print(f"✅ Task {i+1}: {result}")
        except Exception as e:
            results.append(f"Error: {e}")
            print(f"❌ Task {i+1}: {e}")
    
    print(f"📊 Final results: {len([r for r in results if not r.startswith('Error')])} successful")

async def demonstrate_timeout_handling():
    """Shows comprehensive timeout handling strategies"""
    
    async def slow_operation(operation_id, duration):
        print(f"🐌 Operation {operation_id}: Starting ({duration}s)")
        await asyncio.sleep(duration)
        print(f"✅ Operation {operation_id}: Completed")
        return f"Result from {operation_id}"
    
    print("\n=== Timeout Handling Strategies ===")
    
    # Strategy 1: Individual operation timeout
    print("🧪 Individual operation timeout:")
    try:
        result = await asyncio.wait_for(
            slow_operation("Slow1", 3),
            timeout=2.0
        )
        print(f"✅ Result: {result}")
    except asyncio.TimeoutError:
        print("⏰ Operation timed out")
    
    # Strategy 2: Partial completion with timeout
    print("\n🧪 Partial completion with timeout:")
    operations = [
        slow_operation("Op1", 1),    # Will complete
        slow_operation("Op2", 2),    # Will complete  
        slow_operation("Op3", 4),    # Will timeout
        slow_operation("Op4", 5),    # Will timeout
    ]
    
    try:
        completed, pending = await asyncio.wait(
            operations,
            timeout=2.5,
            return_when=asyncio.ALL_COMPLETED
        )
        
        print(f"📊 Completed: {len(completed)}, Pending: {len(pending)}")
        
        # Process completed tasks
        for task in completed:
            try:
                result = await task
                print(f"✅ Completed: {result}")
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        # Cancel pending tasks
        for task in pending:
            task.cancel()
        
        # Wait for cancellation to complete
        if pending:
            await asyncio.wait(pending)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def demonstrate_resilient_patterns():
    """Shows patterns for building resilient async applications"""
    
    async def unreliable_service_call(call_id):
        """Simulates an unreliable external service"""
        await asyncio.sleep(0.1)
        if random.random() < 0.7:  # 70% failure rate
            raise ConnectionError(f"Service call {call_id} failed")
        return f"Service result {call_id}"
    
    async def retry_with_backoff(operation, max_retries=3, base_delay=0.1):
        """Retry an operation with exponential backoff"""
        for attempt in range(max_retries + 1):
            try:
                return await operation()
            except Exception as e:
                if attempt == max_retries:
                    raise  # Final attempt failed
                
                delay = base_delay * (2 ** attempt)  # Exponential backoff
                print(f"⚠️  Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                await asyncio.sleep(delay)
    
    async def circuit_breaker_call(service_func, failure_threshold=3):
        """Simple circuit breaker pattern"""
        if not hasattr(circuit_breaker_call, 'failures'):
            circuit_breaker_call.failures = 0
            circuit_breaker_call.last_failure_time = 0
        
        # Check if circuit is open
        if circuit_breaker_call.failures >= failure_threshold:
            time_since_failure = asyncio.get_event_loop().time() - circuit_breaker_call.last_failure_time
            if time_since_failure < 5.0:  # 5 second timeout
                raise Exception("Circuit breaker is OPEN - service unavailable")
            else:
                # Reset circuit breaker
                circuit_breaker_call.failures = 0
        
        try:
            result = await service_func()
            circuit_breaker_call.failures = 0  # Reset on success
            return result
        except Exception as e:
            circuit_breaker_call.failures += 1
            circuit_breaker_call.last_failure_time = asyncio.get_event_loop().time()
            raise
    
    print("\n=== Resilient Service Calls ===")
    
    # Test retry pattern
    print("🔄 Testing retry with backoff:")
    try:
        result = await retry_with_backoff(
            lambda: unreliable_service_call("RetryTest"),
            max_retries=3
        )
        print(f"✅ Retry succeeded: {result}")
    except Exception as e:
        print(f"❌ All retries failed: {e}")
    
    # Test circuit breaker pattern
    print("\n🔌 Testing circuit breaker:")
    for i in range(8):
        try:
            result = await circuit_breaker_call(
                lambda: unreliable_service_call(f"CB-{i}")
            )
            print(f"✅ Call {i}: {result}")
        except Exception as e:
            print(f"❌ Call {i}: {e}")

async def main():
    await demonstrate_exception_propagation()
    await demonstrate_task_exception_handling()
    await demonstrate_timeout_handling()
    await demonstrate_resilient_patterns()

asyncio.run(main())
```

## Performance Optimization and Best Practices

Understanding asyncio performance characteristics helps you build efficient applications.

### Connection Pooling and Resource Management

```python
import asyncio
import aiohttp
import time

class HighPerformanceHTTPClient:
    """Demonstrates proper resource management and connection pooling"""
    
    def __init__(self, max_connections=100, requests_per_host=30):
        # Configure connection pooling
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,           # Total connection pool size
            limit_per_host=requests_per_host, # Connections per host
            keepalive_timeout=30,            # Keep connections alive
            enable_cleanup_closed=True,      # Clean up closed connections
            use_dns_cache=True,              # Cache DNS lookups
            ttl_dns_cache=300                # DNS cache TTL
        )
        
        # Configure timeouts
        self.timeout = aiohttp.ClientTimeout(
            total=30,      # Total request timeout
            connect=5,     # Connection timeout
            sock_read=10   # Socket read timeout
        )
        
        self.session = None
        self.request_count = 0
        self.connection_stats = {"created": 0, "reused": 0}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        await self.connector.close()
    
    async def get(self, url, **kwargs):
        """Make GET request with connection reuse"""
        self.request_count += 1
        
        async with self.session.get(url, **kwargs) as response:
            # Track connection reuse
            connection_key = response.connection.key
            if hasattr(self, '_seen_connections'):
                if connection_key in self._seen_connections:
                    self.connection_stats["reused"] += 1
                else:
                    self.connection_stats["created"] += 1
                    self._seen_connections.add(connection_key)
            else:
                self._seen_connections = {connection_key}
                self.connection_stats["created"] += 1
            
            return await response.json()
    
    def get_stats(self):
        """Get performance statistics"""
        return {
            "total_requests": self.request_count,
            "connections_created": self.connection_stats["created"],
            "connections_reused": self.connection_stats["reused"],
            "reuse_rate": self.connection_stats["reused"] / max(1, self.request_count) * 100
        }

async def demonstrate_connection_pooling():
    """Shows the benefits of connection pooling"""
    
    print("=== Connection Pooling Performance ===")
    
    async def test_with_pooling():
        """Test with proper connection pooling"""
        async with HighPerformanceHTTPClient(max_connections=10) as client:
            start_time = time.time()
            
            # Make many requests to the same host
            tasks = [
                client.get(f"https://httpbin.org/get?id={i}")
                for i in range(20)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            duration = time.time() - start_time
            stats = client.get_stats()
            
            successful = len([r for r in results if not isinstance(r, Exception)])
            
            return {
                "duration": duration,
                "successful_requests": successful,
                "stats": stats
            }
    
    async def test_without_pooling():
        """Test without connection pooling (creates new session each time)"""
        async def single_request(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
        
        start_time = time.time()
        
        tasks = [
            single_request(f"https://httpbin.org/get?id={i}")
            for i in range(20)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        duration = time.time() - start_time
        successful = len([r for r in results if not isinstance(r, Exception)])
        
        return {
            "duration": duration,
            "successful_requests": successful,
            "stats": {"note": "No pooling - each request creates new connection"}
        }
    
    # Test both approaches
    print("🔄 Testing WITH connection pooling:")
    pooled_results = await test_with_pooling()
    
    print("🔄 Testing WITHOUT connection pooling:")
    no_pool_results = await test_without_pooling()
    
    # Compare results
    print(f"\n📊 Performance Comparison:")
    print(f"  With pooling:    {pooled_results['duration']:.2f}s for {pooled_results['successful_requests']} requests")
    print(f"  Without pooling: {no_pool_results['duration']:.2f}s for {no_pool_results['successful_requests']} requests")
    print(f"  Speedup: {no_pool_results['duration'] / pooled_results['duration']:.1f}x")
    
    print(f"\n🔌 Connection Statistics:")
    stats = pooled_results['stats']
    print(f"  Connections created: {stats['connections_created']}")
    print(f"  Connections reused: {stats['connections_reused']}")
    print(f"  Reuse rate: {stats['reuse_rate']:.1f}%")

async def demonstrate_batching_optimization():
    """Shows the performance benefits of batching operations"""
    
    async def process_item(item_id):
        """Simulate processing a single item"""
        await asyncio.sleep(0.1)  # Simulate processing time
        return f"Processed-{item_id}"
    
    async def process_batch(item_ids):
        """Simulate processing a batch of items (more efficient)"""
        await asyncio.sleep(0.05 * len(item_ids))  # Batch processing is more efficient
        return [f"BatchProcessed-{item_id}" for item_id in item_ids]
    
    print("\n=== Batching vs Individual Processing ===")
    
    items = list(range(1, 21))  # 20 items to process
    
    # Individual processing
    print("🔄 Individual processing:")
    start_time = time.time()
    individual_results = await asyncio.gather(*[
        process_item(item_id) for item_id in items
    ])
    individual_time = time.time() - start_time
    
    # Batch processing
    print("🔄 Batch processing:")
    batch_size = 5
    batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
    
    start_time = time.time()
    batch_results = await asyncio.gather(*[
        process_batch(batch) for batch in batches
    ])
    # Flatten results
    batch_results_flat = [item for batch in batch_results for item in batch]
    batch_time = time.time() - start_time
    
    print(f"\n📊 Batching Performance:")
    print(f"  Individual: {individual_time:.2f}s for {len(individual_results)} items")
    print(f"  Batched:    {batch_time:.2f}s for {len(batch_results_flat)} items")
    print(f"  Speedup: {individual_time / batch_time:.1f}x")

async def demonstrate_memory_efficient_streaming():
    """Shows memory-efficient processing of large datasets"""
    
    async def generate_large_dataset():
        """Simulate a large data source"""
        for i in range(10000):  # Large dataset
            yield {"id": i, "data": f"item_{i}", "value": i * 2}
            # Small delay to simulate real data source
            if i % 100 == 0:
                await asyncio.sleep(0.001)
    
    async def process_streaming_data():
        """Process data as it arrives (memory efficient)"""
        processed_count = 0
        total_value = 0
        
        async for item in generate_large_dataset():
            # Process each item as it arrives
            total_value += item["value"]
            processed_count += 1
            
            if processed_count % 1000 == 0:
                print(f"📊 Processed {processed_count} items (streaming)")
        
        return {"count": processed_count, "total_value": total_value}
    
    async def process_batch_loaded_data():
        """Load all data then process (memory intensive)"""
        # Load all data into memory
        all_data = []
        async for item in generate_large_dataset():
            all_data.append(item)
        
        print(f"📊 Loaded {len(all_data)} items into memory")
        
        # Process all data
        total_value = sum(item["value"] for item in all_data)
        
        return {"count": len(all_data), "total_value": total_value}
    
    print("\n=== Memory-Efficient Streaming ===")
    
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    # Test streaming approach
    print("🌊 Streaming processing:")
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    streaming_result = await process_streaming_data()
    
    streaming_time = time.time() - start_time
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    memory_used_streaming = memory_after - memory_before
    
    # Test batch loading approach
    print("📦 Batch loading processing:")
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    batch_result = await process_batch_loaded_data()
    
    batch_time = time.time() - start_time
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    memory_used_batch = memory_after - memory_before
    
    print(f"\n📊 Memory and Performance Comparison:")
    print(f"  Streaming: {streaming_time:.2f}s, ~{memory_used_streaming:.1f}MB extra memory")
    print(f"  Batch:     {batch_time:.2f}s, ~{memory_used_batch:.1f}MB extra memory")
    print(f"  Memory savings with streaming: {memory_used_batch - memory_used_streaming:.1f}MB")

async def main():
    await demonstrate_connection_pooling()
    await demonstrate_batching_optimization()
    await demonstrate_memory_efficient_streaming()

asyncio.run(main())
```

## Common Pitfalls and Solutions

Understanding common mistakes helps you write better asyncio code.

### Blocking the Event Loop

```python
import asyncio
import time
import requests
import aiohttp
import concurrent.futures

async def demonstrate_blocking_problems():
    """Shows how blocking calls break asyncio's concurrency"""
    
    print("=== The Blocking Problem ===")
    
    async def bad_concurrent_requests():
        """❌ DON'T DO THIS - blocking calls in async code"""
        print("🐌 Making 'concurrent' requests with blocking library...")
        start_time = time.time()
        
        # These look concurrent but actually run sequentially!
        tasks = []
        for i in range(3):
            # requests.get() is a blocking call that stops the entire event loop
            task = asyncio.create_task(
                asyncio.to_thread(  # We'll fix this in the good example
                    requests.get, f"https://httpbin.org/delay/1"
                )
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        duration = time.time() - start_time
        print(f"🐌 'Concurrent' requests took: {duration:.2f}s")
        return duration
    
    async def truly_blocking_example():
        """❌ What NOT to do - direct blocking calls"""
        print("🚫 Direct blocking calls (DON'T DO THIS):")
        start_time = time.time()
        
        # This completely blocks the event loop!
        # We'll simulate this with a CPU-intensive task
        def cpu_intensive_work():
            total = 0
            for i in range(1000000):
                total += i ** 2
            return total
        
        # This blocks everything
        result = cpu_intensive_work()
        duration = time.time() - start_time
        print(f"🚫 Blocking operation took: {duration:.2f}s")
        return duration
    
    async def good_concurrent_requests():
        """✅ DO THIS - proper async requests"""
        print("🚀 Making truly concurrent requests...")
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                session.get(f"https://httpbin.org/delay/1")
                for _ in range(3)
            ]
            
            responses = await asyncio.gather(*tasks)
            
            # Close responses
            for response in responses:
                response.close()
        
        duration = time.time() - start_time
        print(f"🚀 Truly concurrent requests took: {duration:.2f}s")
        return duration
    
    async def good_cpu_intensive_work():
        """✅ DO THIS - CPU work in executor"""
        print("⚡ CPU work in executor:")
        start_time = time.time()
        
        def cpu_intensive_work():
            total = 0
            for i in range(1000000):
                total += i ** 2
            return total
        
        # Run CPU work in thread pool
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, cpu_intensive_work)
        
        duration = time.time() - start_time
        print(f"⚡ Non-blocking CPU work took: {duration:.2f}s")
        return duration
    
    # Compare approaches
    good_requests_time = await good_concurrent_requests()
    bad_requests_time = await bad_concurrent_requests()
    
    print(f"\n📊 Request Performance:")
    print(f"  Speedup with proper async: {bad_requests_time / good_requests_time:.1f}x")
    
    blocking_time = await truly_blocking_example()
    nonblocking_time = await good_cpu_intensive_work()
    
    print(f"\n📊 CPU Work Performance:")
    print(f"  Both approaches took similar time, but async version doesn't block the event loop")

async def demonstrate_resource_leaks():
    """Shows resource leak problems and solutions"""
    
    print("\n=== Resource Management ===")
    
    async def resource_leak_example():
        """❌ Resource leak example"""
        print("🚨 Resource leak example (DON'T DO THIS):")
        
        sessions = []
        for i in range(5):
            # Creating sessions but not closing them!
            session = aiohttp.ClientSession()
            sessions.append(session)
            
            try:
                async with session.get("https://httpbin.org/get") as response:
                    data = await response.json()
                    print(f"  Request {i+1}: Status {response.status}")
            except Exception as e:
                print(f"  Request {i+1}: Error {e}")
        
        # Sessions are never closed - RESOURCE LEAK!
        print("🚨 Sessions created but never closed - memory and connection leak!")
        
        # Clean up for demo (you shouldn't rely on this)
        for session in sessions:
            await session.close()
    
    async def proper_resource_management():
        """✅ Proper resource management"""
        print("✅ Proper resource management:")
        
        # Method 1: Context manager (preferred)
        async with aiohttp.ClientSession() as session:
            tasks = [
                session.get("https://httpbin.org/get")
                for _ in range(5)
            ]
            
            responses = await asyncio.gather(*tasks)
            
            for i, response in enumerate(responses):
                print(f"  Request {i+1}: Status {response.status}")
                response.close()
        
        # Session automatically closed by context manager
        print("✅ Session automatically closed by context manager")
    
    async def manual_cleanup_example():
        """✅ Manual cleanup when context manager not available"""
        print("✅ Manual cleanup example:")
        
        session = aiohttp.ClientSession()
        try:
            async with session.get("https://httpbin.org/get") as response:
                data = await response.json()
                print(f"  Manual cleanup: Status {response.status}")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            await session.close()  # Always close in finally block
            print("✅ Session manually closed in finally block")
    
    await resource_leak_example()
    await proper_resource_management()
    await manual_cleanup_example()

async def demonstrate_deadlock_avoidance():
    """Shows how to avoid deadlocks in async code"""
    
    print("\n=== Deadlock Avoidance ===")
    
    async def deadlock_example():
        """⚠️ Potential deadlock scenario"""
        lock1 = asyncio.Lock()
        lock2 = asyncio.Lock()
        
        async def task_a():
            async with lock1:
                print("🔒 Task A: Acquired lock1")
                await asyncio.sleep(0.1)
                
                # Try to acquire lock2 while holding lock1
                print("🔒 Task A: Trying to acquire lock2...")
                async with lock2:
                    print("🔒 Task A: Acquired lock2")
        
        async def task_b():
            async with lock2:
                print("🔒 Task B: Acquired lock2")
                await asyncio.sleep(0.1)
                
                # Try to acquire lock1 while holding lock2
                print("🔒 Task B: Trying to acquire lock1...")
                async with lock1:
                    print("🔒 Task B: Acquired lock1")
        
        print("⚠️ Potential deadlock scenario (tasks acquire locks in different order):")
        
        try:
            # This might deadlock!
            await asyncio.wait_for(
                asyncio.gather(task_a(), task_b()),
                timeout=1.0
            )
            print("✅ No deadlock occurred")
        except asyncio.TimeoutError:
            print("❌ Deadlock detected! Tasks timed out")
    
    async def deadlock_solution():
        """✅ Deadlock-free solution"""
        lock1 = asyncio.Lock()
        lock2 = asyncio.Lock()
        
        async def safe_task_a():
            # Always acquire locks in the same order
            async with lock1:
                print("✅ Safe Task A: Acquired lock1")
                async with lock2:
                    print("✅ Safe Task A: Acquired lock2")
                    await asyncio.sleep(0.1)
        
        async def safe_task_b():
            # Same order as task A
            async with lock1:
                print("✅ Safe Task B: Acquired lock1")
                async with lock2:
                    print("✅ Safe Task B: Acquired lock2")
                    await asyncio.sleep(0.1)
        
        print("✅ Deadlock-free solution (consistent lock ordering):")
        await asyncio.gather(safe_task_a(), safe_task_b())
        print("✅ All tasks completed successfully")
    
    await deadlock_example()
    await deadlock_solution()

async def demonstrate_forgotten_await():
    """Shows the consequences of forgetting await"""
    
    print("\n=== Forgotten await Problems ===")
    
    async def important_async_function():
        """An async function that should be awaited"""
        await asyncio.sleep(0.1)
        return "Important result"
    
    async def forgot_await_example():
        """❌ Forgetting to await"""
        print("❌ Forgetting to await:")
        
        # This doesn't actually run the function!
        result = important_async_function()  # Returns coroutine object
        print(f"  Result type: {type(result)}")
        print(f"  Result value: {result}")
        print("  ⚠️ The function never actually executed!")
        
        # Clean up to prevent warning
        result.close()
    
    async def correct_await_example():
        """✅ Proper await usage"""
        print("✅ Proper await usage:")
        
        result = await important_async_function()  # Actually runs the function
        print(f"  Result: {result}")
        print("  ✅ Function executed and returned result")
    
    async def loop_await_mistake():
        """❌ Common mistake in loops"""
        print("❌ Forgetting await in loops:")
        
        coroutines = []
        for i in range(3):
            # This creates coroutine objects but doesn't run them
            coro = important_async_function()
            coroutines.append(coro)
        
        print(f"  Created {len(coroutines)} coroutine objects")
        print("  ⚠️ None of them have executed yet!")
        
        # Clean up
        for coro in coroutines:
            coro.close()
    
    async def correct_loop_example():
        """✅ Correct loop with await"""
        print("✅ Correct loop with concurrent execution:")
        
        # Create tasks that start immediately
        tasks = [
            asyncio.create_task(important_async_function())
            for _ in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"  Results: {results}")
        print("  ✅ All functions executed concurrently")
    
    await forgot_await_example()
    await correct_await_example()
    await loop_await_mistake()
    await correct_loop_example()

async def main():
    await demonstrate_blocking_problems()
    await demonstrate_resource_leaks()
    await demonstrate_deadlock_avoidance()
    await demonstrate_forgotten_await()

asyncio.run(main())
```

## Real-World Application Patterns

Here are comprehensive patterns for building production asyncio applications:

### Web Scraping with Rate Limiting

```python
import asyncio
import aiohttp
import time
from urllib.parse import urljoin, urlparse
import random

class IntelligentWebScraper:
    """Production-ready web scraper with rate limiting and error handling"""
    
    def __init__(self, base_delay=1.0, max_concurrent=5, max_retries=3):
        self.base_delay = base_delay
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.session = None
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # Statistics
        self.stats = {
            "requests_made": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "retries": 0,
            "rate_limited": 0
        }
        
        # Rate limiting per domain
        self.last_request_time = {}
        self.domain_delays = {}
    
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=50,
            limit_per_host=10,
            keepalive_timeout=30
        )
        
        timeout = aiohttp.ClientTimeout(total=30)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; AsyncScraper/1.0)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def smart_delay(self, url):
        """Implement intelligent rate limiting per domain"""
        domain = urlparse(url).netloc
        
        # Get domain-specific delay
        domain_delay = self.domain_delays.get(domain, self.base_delay)
        
        # Check if we need to wait
        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < domain_delay:
                wait_time = domain_delay - elapsed
                print(f"⏰ Rate limiting: waiting {wait_time:.1f}s for {domain}")
                await asyncio.sleep(wait_time)
                self.stats["rate_limited"] += 1
        
        self.last_request_time[domain] = time.time()
    
    async def fetch_with_retries(self, url):
        """Fetch URL with intelligent retry logic"""
        domain = urlparse(url).netloc
        
        for attempt in range(self.max_retries + 1):
            try:
                async with self.semaphore:  # Limit concurrent requests
                    await self.smart_delay(url)  # Rate limiting
                    
                    self.stats["requests_made"] += 1
                    
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            self.stats["successful_requests"] += 1
                            return {
                                "url": url,
                                "content": content,
                                "status": response.status,
                                "headers": dict(response.headers)
                            }
                        
                        elif response.status == 429:  # Rate limited
                            # Increase delay for this domain
                            self.domain_delays[domain] = self.domain_delays.get(domain, self.base_delay) * 2
                            raise aiohttp.ClientResponseError(
                                request_info=response.request_info,
                                history=response.history,
                                status=response.status,
                                message="Rate limited"
                            )
                        
                        else:
                            raise aiohttp.ClientResponseError(
                                request_info=response.request_info,
                                history=response.history,
                                status=response.status
                            )
            
            except Exception as e:
                self.stats["failed_requests"] += 1
                
                if attempt == self.max_retries:
                    print(f"❌ Failed to fetch {url} after {self.max_retries + 1} attempts: {e}")
                    return None
                
                # Exponential backoff
                retry_delay = (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ Attempt {attempt + 1} failed for {url}: {e}. Retrying in {retry_delay:.1f}s...")
                self.stats["retries"] += 1
                await asyncio.sleep(retry_delay)
        
        return None

async def demonstrate_intelligent_scraping():
    """Demonstrates intelligent web scraping"""
    
    print("=== Intelligent Web Scraping ===")
    
    # URLs to scrape
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/json",
        "https://httpbin.org/headers",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/429",  # Rate limited response
        "https://httpbin.org/html",
    ]
    
    async with IntelligentWebScraper(base_delay=0.5, max_concurrent=3) as scraper:
        start_time = time.time()
        
        # Scrape all URLs concurrently with rate limiting
        tasks = [scraper.fetch_with_retries(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        duration = time.time() - start_time
        
        # Analyze results
        successful = [r for r in results if r is not None]
        failed = [r for r in results if r is None]
        
        print(f"\n📊 Scraping Results:")
        print(f"  Duration: {duration:.2f}s")
        print(f"  Successful: {len(successful)}")
        print(f"  Failed: {len(failed)}")
        print(f"  Total requests made: {scraper.stats['requests_made']}")
        print(f"  Rate limited events: {scraper.stats['rate_limited']}")
        print(f"  Retries performed: {scraper.stats['retries']}")
        
        # Show successful results
        for result in successful[:3]:  # Show first 3
            print(f"  ✅ {result['url']}: {result['status']} ({len(result['content'])} chars)")

asyncio.run(demonstrate_intelligent_scraping())
```

This regenerated asyncio cheatsheet provides a comprehensive, deep-dive exploration of asyncio concepts with working examples and practical patterns. It maintains the focus on explaining how things work rather than just listing tips, making it an excellent learning and reference resource.

