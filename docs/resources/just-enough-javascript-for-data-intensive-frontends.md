# Just Enough JavaScript for Data-Intensive Frontends


!!! note "AI Generated (Claude Sonnet 4.5)"

Building frontends for data-intensive applications requires understanding how JavaScript handles data flow, reactivity, and performance. This guide focuses on the core concepts you need to build real-time dashboards, analytics platforms, and data visualization tools using React—the most popular framework for these use cases.

## Table of Contents
1. JavaScript Fundamentals That Matter
2. Asynchronous JavaScript for Real-Time Data
3. React Essentials for Data Applications
4. State Management for Complex Data
5. Performance Optimization Techniques
6. Real-Time Data Patterns

---

## 1. JavaScript Fundamentals That Matter

### Arrays and Data Transformation

When working with data, you'll constantly transform, filter, and aggregate arrays. Here are the essential methods:

```javascript
// Sample dataset: sales transactions
const transactions = [
  { id: 1, product: 'Laptop', amount: 1200, timestamp: '2024-01-15T10:30:00Z' },
  { id: 2, product: 'Mouse', amount: 25, timestamp: '2024-01-15T11:00:00Z' },
  { id: 3, product: 'Keyboard', amount: 75, timestamp: '2024-01-15T11:30:00Z' },
  { id: 4, product: 'Laptop', amount: 1200, timestamp: '2024-01-15T12:00:00Z' }
];

// Filter: Get only high-value transactions
const highValueTransactions = transactions.filter(t => t.amount > 100);
// Returns: [{ id: 1, ...}, { id: 3, ...}, { id: 4, ...}]

// Map: Extract just the amounts
const amounts = transactions.map(t => t.amount);
// Returns: [1200, 25, 75, 1200]

// Reduce: Calculate total revenue
const totalRevenue = transactions.reduce((sum, t) => sum + t.amount, 0);
// Returns: 2500

// Chaining: Get total revenue from laptops only
const laptopRevenue = transactions
  .filter(t => t.product === 'Laptop')
  .reduce((sum, t) => sum + t.amount, 0);
// Returns: 2400
```

**How it works:** Each method returns a new array (or value) without modifying the original. This is crucial for React's rendering optimization, which relies on detecting changes by comparing references.

### Object Destructuring and Spread Operator

These syntaxes make data manipulation cleaner:

```javascript
// Destructuring: Extract properties
const transaction = { id: 1, product: 'Laptop', amount: 1200 };
const { product, amount } = transaction;
// product = 'Laptop', amount = 1200

// Spread operator: Merge or update objects
const updatedTransaction = { ...transaction, status: 'completed' };
// Creates new object with all transaction properties plus status

// Array spread: Combine datasets
const morningData = [1, 2, 3];
const afternoonData = [4, 5, 6];
const fullDayData = [...morningData, ...afternoonData];
// Returns: [1, 2, 3, 4, 5, 6]

// Practical example: Adding new data point
const [dataPoints, setDataPoints] = useState([]);
setDataPoints([...dataPoints, newDataPoint]); // Appends to existing array
```

**Why this matters:** The spread operator creates new objects/arrays, which triggers React re-renders properly. Mutating existing objects directly won't trigger updates.

### Template Literals for Dynamic Strings

```javascript
const value = 1250.50;
const timestamp = new Date().toLocaleTimeString();

// Old way
const message = "Value: $" + value.toFixed(2) + " at " + timestamp;

// Modern way
const message = `Value: $${value.toFixed(2)} at ${timestamp}`;

// Multi-line strings (useful for API queries)
const graphQLQuery = `
  query {
    transactions(limit: 100) {
      id
      amount
      timestamp
    }
  }
`;
```

---

## 2. Asynchronous JavaScript for Real-Time Data

### Promises and Async/Await

Data-intensive apps constantly fetch data from APIs. Understanding asynchronous code is essential:

```javascript
// Promise-based fetch
function fetchTransactions() {
  return fetch('https://api.example.com/transactions')
    .then(response => response.json())
    .then(data => {
      console.log('Data received:', data);
      return data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Same thing with async/await (cleaner for complex logic)
async function fetchTransactions() {
  try {
    const response = await fetch('https://api.example.com/transactions');
    const data = await response.json();
    console.log('Data received:', data);
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

**How it works:** JavaScript is single-threaded, but `async/await` allows you to write asynchronous code that looks synchronous. The `await` keyword pauses execution until the Promise resolves, without blocking the entire application.

### Real-Time Data with WebSockets

For live updates (stock prices, sensor data, chat messages), WebSockets provide two-way communication:

```javascript
// Establishing WebSocket connection
const socket = new WebSocket('wss://api.example.com/realtime');

// Handle connection open
socket.addEventListener('open', (event) => {
  console.log('Connected to WebSocket');
  socket.send(JSON.stringify({ type: 'subscribe', channel: 'trades' }));
});

// Receive messages
socket.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log('New trade:', data);
  // Update your UI state here
});

// Handle errors
socket.addEventListener('error', (error) => {
  console.error('WebSocket error:', error);
});

// Clean up on disconnect
socket.addEventListener('close', () => {
  console.log('WebSocket disconnected');
  // Implement reconnection logic here
});
```

### Server-Sent Events (SSE) - Simpler Alternative

For one-way server-to-client updates, SSE is simpler than WebSockets:

```javascript
const eventSource = new EventSource('https://api.example.com/events');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update received:', data);
};

eventSource.onerror = (error) => {
  console.error('SSE error:', error);
  eventSource.close();
};
```

**When to use what:** Use SSE for server-to-client updates (dashboards, notifications). Use WebSockets when you need bidirectional communication (collaborative editing, real-time chat).

---

## 3. React Essentials for Data Applications

### Component Basics

React components are JavaScript functions that return UI. Think of them as reusable templates:

```javascript
// Simple component displaying a metric
function MetricCard({ title, value, change }) {
  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <div className="value">${value.toLocaleString()}</div>
      <div className={`change ${change >= 0 ? 'positive' : 'negative'}`}>
        {change >= 0 ? '↑' : '↓'} {Math.abs(change)}%
      </div>
    </div>
  );
}

// Using the component
function Dashboard() {
  return (
    <div>
      <MetricCard title="Revenue" value={125000} change={12.5} />
      <MetricCard title="Expenses" value={75000} change={-3.2} />
    </div>
  );
}
```

### useState: Managing Component Data

`useState` is React's way of tracking data that changes over time:

```javascript
import { useState } from 'react';

function LiveCounter() {
  // useState returns [currentValue, functionToUpdateValue]
  const [count, setCount] = useState(0);
  const [transactions, setTransactions] = useState([]);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

**How it works:** When you call `setCount`, React re-renders the component with the new value. The component function runs again, but `useState` remembers the previous value.

### useEffect: Side Effects and Data Fetching

`useEffect` runs code after rendering—perfect for fetching data, setting up subscriptions, or timers:

```javascript
import { useState, useEffect } from 'react';

function TransactionList() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // This runs after the component renders
    async function loadData() {
      try {
        const response = await fetch('https://api.example.com/transactions');
        const data = await response.json();
        setTransactions(data);
      } catch (error) {
        console.error('Failed to fetch:', error);
      } finally {
        setLoading(false);
      }
    }
    
    loadData();
  }, []); // Empty array = run once on mount
  
  if (loading) return <div>Loading...</div>;
  
  return (
    <ul>
      {transactions.map(t => (
        <li key={t.id}>{t.product}: ${t.amount}</li>
      ))}
    </ul>
  );
}
```

**Dependency array explained:**
- `[]` - Run once when component mounts
- `[value]` - Run when `value` changes
- No array - Run after every render (usually not what you want!)

### Real-Time Updates with useEffect

Here's a complete example connecting to a WebSocket:

```javascript
import { useState, useEffect } from 'react';

function LivePriceTracker({ symbol }) {
  const [price, setPrice] = useState(null);
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    const socket = new WebSocket(`wss://api.example.com/prices/${symbol}`);
    
    socket.addEventListener('open', () => {
      setConnected(true);
      console.log(`Connected to ${symbol} price feed`);
    });
    
    socket.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      setPrice(data.price);
    });
    
    socket.addEventListener('close', () => {
      setConnected(false);
    });
    
    // Cleanup function: runs when component unmounts or dependencies change
    return () => {
      socket.close();
      console.log('Disconnected from price feed');
    };
  }, [symbol]); // Reconnect if symbol changes
  
  return (
    <div>
      <h2>{symbol}</h2>
      <div className={`status ${connected ? 'online' : 'offline'}`}>
        {connected ? '🟢 Live' : '🔴 Offline'}
      </div>
      {price && <div className="price">${price.toFixed(2)}</div>}
    </div>
  );
}
```

**Why the cleanup function:** When the component unmounts or `symbol` changes, we need to close the old WebSocket connection to prevent memory leaks.

---

## 4. State Management for Complex Data

### Local State vs. Shared State

For simple apps, `useState` in individual components works fine. But data-intensive apps often need to share data across many components.

**Problem:** Passing data through many component levels (prop drilling)

```javascript
// Prop drilling - data passes through components that don't need it
function Dashboard() {
  const [userData, setUserData] = useState(null);
  
  return <Sidebar userData={userData} />;
}

function Sidebar({ userData }) {
  return <UserMenu userData={userData} />; // Just passing it along
}

function UserMenu({ userData }) {
  return <div>{userData.name}</div>; // Finally using it
}
```

### React Context for Shared Data

Context lets you share data without passing props through every level:

```javascript
import { createContext, useContext, useState } from 'react';

// Create context
const DataContext = createContext();

// Provider component wraps your app
function DataProvider({ children }) {
  const [transactions, setTransactions] = useState([]);
  const [metrics, setMetrics] = useState({ revenue: 0, count: 0 });
  
  return (
    <DataContext.Provider value={{ transactions, setTransactions, metrics, setMetrics }}>
      {children}
    </DataContext.Provider>
  );
}

// Custom hook to use the context
function useData() {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within DataProvider');
  }
  return context;
}

// Now any component can access the data
function TransactionSummary() {
  const { transactions, metrics } = useData();
  
  return (
    <div>
      <h3>Total Transactions: {transactions.length}</h3>
      <h3>Revenue: ${metrics.revenue}</h3>
    </div>
  );
}

// Wrap your app
function App() {
  return (
    <DataProvider>
      <Dashboard />
      <TransactionSummary />
    </DataProvider>
  );
}
```

### Custom Hooks for Reusable Logic

Extract common patterns into custom hooks:

```javascript
// Custom hook for fetching data
function useDataFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [url]);
  
  return { data, loading, error };
}

// Use it in any component
function DataDisplay() {
  const { data, loading, error } = useDataFetch('https://api.example.com/data');
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return <div>{JSON.stringify(data)}</div>;
}
```

### Custom Hook for WebSocket

```javascript
function useWebSocket(url) {
  const [data, setData] = useState(null);
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    const socket = new WebSocket(url);
    
    socket.onopen = () => setConnected(true);
    socket.onmessage = (event) => setData(JSON.parse(event.data));
    socket.onclose = () => setConnected(false);
    
    return () => socket.close();
  }, [url]);
  
  return { data, connected };
}

// Usage
function LiveDashboard() {
  const { data, connected } = useWebSocket('wss://api.example.com/live');
  
  return (
    <div>
      {connected ? '🟢 Connected' : '🔴 Disconnected'}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}
```

---

## 5. Performance Optimization Techniques

### useMemo: Expensive Calculations

When you have computationally expensive operations, `useMemo` prevents recalculating on every render:

```javascript
import { useMemo } from 'react';

function SalesAnalytics({ transactions }) {
  // This calculation only runs when transactions change
  const analytics = useMemo(() => {
    console.log('Calculating analytics...');
    
    const totalRevenue = transactions.reduce((sum, t) => sum + t.amount, 0);
    const avgTransaction = totalRevenue / transactions.length;
    const topProducts = transactions
      .reduce((acc, t) => {
        acc[t.product] = (acc[t.product] || 0) + t.amount;
        return acc;
      }, {});
    
    return { totalRevenue, avgTransaction, topProducts };
  }, [transactions]); // Only recalculate when transactions changes
  
  return (
    <div>
      <p>Revenue: ${analytics.totalRevenue}</p>
      <p>Avg Transaction: ${analytics.avgTransaction.toFixed(2)}</p>
    </div>
  );
}
```

**Without useMemo:** The calculation runs on every render, even if `transactions` hasn't changed.

**With useMemo:** The calculation only runs when `transactions` actually changes.

### useCallback: Preventing Unnecessary Re-renders

`useCallback` memoizes function references, useful when passing callbacks to child components:

```javascript
import { useState, useCallback } from 'react';

function DataTable({ data }) {
  const [sortBy, setSortBy] = useState('date');
  
  // This function reference stays the same unless sortBy changes
  const handleSort = useCallback((column) => {
    setSortBy(column);
  }, []);
  
  // Without useCallback, this creates a new function every render,
  // causing child components to re-render unnecessarily
  
  return (
    <table>
      <TableHeader onSort={handleSort} />
      <TableBody data={data} sortBy={sortBy} />
    </table>
  );
}
```

### React.memo: Preventing Component Re-renders

Wrap components to prevent re-rendering when props haven't changed:

```javascript
import { memo } from 'react';

// This component only re-renders when price or symbol changes
const PriceDisplay = memo(function PriceDisplay({ symbol, price }) {
  console.log(`Rendering ${symbol}`);
  return (
    <div>
      {symbol}: ${price.toFixed(2)}
    </div>
  );
});

function Dashboard() {
  const [btcPrice, setBtcPrice] = useState(50000);
  const [ethPrice, setEthPrice] = useState(3000);
  const [counter, setCounter] = useState(0);
  
  return (
    <div>
      {/* These only re-render when their specific price changes */}
      <PriceDisplay symbol="BTC" price={btcPrice} />
      <PriceDisplay symbol="ETH" price={ethPrice} />
      
      {/* This button changes counter, but PriceDisplay components don't re-render */}
      <button onClick={() => setCounter(counter + 1)}>
        Counter: {counter}
      </button>
    </div>
  );
}
```

### Virtual Scrolling for Large Datasets

When displaying thousands of rows, render only visible items:

```javascript
import { useState, useRef, useEffect } from 'react';

function VirtualList({ items, itemHeight = 50 }) {
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef(null);
  const containerHeight = 600; // viewport height
  
  // Calculate which items are visible
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    items.length,
    Math.ceil((scrollTop + containerHeight) / itemHeight)
  );
  
  const visibleItems = items.slice(startIndex, endIndex);
  
  // Total height of all items
  const totalHeight = items.length * itemHeight;
  
  // Offset for visible items
  const offsetY = startIndex * itemHeight;
  
  return (
    <div
      ref={containerRef}
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, index) => (
            <div
              key={startIndex + index}
              style={{ height: itemHeight }}
            >
              {item.name} - ${item.value}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

**How it works:** Instead of rendering 10,000 rows, we only render the ~12 rows currently visible in the viewport, dramatically improving performance.

---

## 6. Real-Time Data Patterns

### Polling Pattern

Simple approach: periodically fetch new data:

```javascript
function usePolling(fetchFunction, interval = 5000) {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    // Fetch immediately
    fetchFunction().then(setData);
    
    // Then fetch on interval
    const timer = setInterval(() => {
      fetchFunction().then(setData);
    }, interval);
    
    return () => clearInterval(timer);
  }, [fetchFunction, interval]);
  
  return data;
}

// Usage
function LiveMetrics() {
  const metrics = usePolling(
    () => fetch('https://api.example.com/metrics').then(r => r.json()),
    3000 // Poll every 3 seconds
  );
  
  return <div>Active Users: {metrics?.activeUsers}</div>;
}
```

**Pros:** Simple, works with any API  
**Cons:** Wasteful if data doesn't change, delays up to polling interval

### WebSocket with Automatic Reconnection

Production-ready WebSocket hook with reconnection logic:

```javascript
function useWebSocketWithReconnect(url, maxRetries = 5) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('connecting');
  const retriesRef = useRef(0);
  const socketRef = useRef(null);
  
  useEffect(() => {
    function connect() {
      setStatus('connecting');
      const socket = new WebSocket(url);
      socketRef.current = socket;
      
      socket.onopen = () => {
        setStatus('connected');
        retriesRef.current = 0;
      };
      
      socket.onmessage = (event) => {
        setData(JSON.parse(event.data));
      };
      
      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        setStatus('error');
      };
      
      socket.onclose = () => {
        setStatus('disconnected');
        
        // Attempt reconnection with exponential backoff
        if (retriesRef.current < maxRetries) {
          const delay = Math.min(1000 * Math.pow(2, retriesRef.current), 30000);
          console.log(`Reconnecting in ${delay}ms...`);
          
          setTimeout(() => {
            retriesRef.current++;
            connect();
          }, delay);
        } else {
          setStatus('failed');
        }
      };
    }
    
    connect();
    
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [url, maxRetries]);
  
  return { data, status };
}

// Usage
function RealtimeChart() {
  const { data, status } = useWebSocketWithReconnect('wss://api.example.com/live');
  
  return (
    <div>
      <div className={`status-indicator ${status}`}>
        {status === 'connected' && '🟢 Live'}
        {status === 'connecting' && '🟡 Connecting...'}
        {status === 'disconnected' && '🟠 Reconnecting...'}
        {status === 'failed' && '🔴 Connection Failed'}
      </div>
      {data && <Chart data={data} />}
    </div>
  );
}
```

### Optimistic Updates

For better UX, update UI immediately, then sync with server:

```javascript
function useOptimisticUpdate() {
  const [items, setItems] = useState([]);
  const [pending, setPending] = useState(new Set());
  
  async function addItem(newItem) {
    // Generate temporary ID
    const tempId = `temp-${Date.now()}`;
    const optimisticItem = { ...newItem, id: tempId };
    
    // Update UI immediately
    setItems(prev => [...prev, optimisticItem]);
    setPending(prev => new Set(prev).add(tempId));
    
    try {
      // Send to server
      const response = await fetch('https://api.example.com/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newItem)
      });
      
      const savedItem = await response.json();
      
      // Replace temporary item with real one
      setItems(prev => prev.map(item => 
        item.id === tempId ? savedItem : item
      ));
      setPending(prev => {
        const next = new Set(prev);
        next.delete(tempId);
        return next;
      });
    } catch (error) {
      // Rollback on error
      setItems(prev => prev.filter(item => item.id !== tempId));
      setPending(prev => {
        const next = new Set(prev);
        next.delete(tempId);
        return next;
      });
      console.error('Failed to add item:', error);
    }
  }
  
  return { items, pending, addItem };
}
```

### Debouncing User Input

Prevent excessive API calls when user is typing:

```javascript
import { useState, useEffect } from 'react';

function useDebounce(value, delay = 500) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return debouncedValue;
}

// Usage: Search with debouncing
function SearchableDataTable() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, 300);
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    if (debouncedSearch) {
      // Only fires 300ms after user stops typing
      fetch(`https://api.example.com/search?q=${debouncedSearch}`)
        .then(r => r.json())
        .then(setResults);
    }
  }, [debouncedSearch]);
  
  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search..."
      />
      <div>Results: {results.length}</div>
    </div>
  );
}
```

---

## Complete Example: Real-Time Analytics Dashboard

Putting it all together:

```javascript
import { useState, useEffect, useMemo } from 'react';

function AnalyticsDashboard() {
  const [transactions, setTransactions] = useState([]);
  const [liveData, setLiveData] = useState(null);
  const [connected, setConnected] = useState(false);
  
  // Fetch initial data
  useEffect(() => {
    async function loadInitialData() {
      const response = await fetch('https://api.example.com/transactions');
      const data = await response.json();
      setTransactions(data);
    }
    loadInitialData();
  }, []);
  
  // Connect to WebSocket for live updates
  useEffect(() => {
    const socket = new WebSocket('wss://api.example.com/live');
    
    socket.onopen = () => setConnected(true);
    
    socket.onmessage = (event) => {
      const newTransaction = JSON.parse(event.data);
      setLiveData(newTransaction);
      
      // Add to transactions list
      setTransactions(prev => [newTransaction, ...prev].slice(0, 100));
    };
    
    socket.onclose = () => setConnected(false);
    
    return () => socket.close();
  }, []);
  
  // Calculate metrics (memoized)
  const metrics = useMemo(() => {
    const total = transactions.reduce((sum, t) => sum + t.amount, 0);
    const count = transactions.length;
    const average = count > 0 ? total / count : 0;
    
    // Calculate hourly breakdown
    const hourly = transactions.reduce((acc, t) => {
      const hour = new Date(t.timestamp).getHours();
      acc[hour] = (acc[hour] || 0) + t.amount;
      return acc;
    }, {});
    
    return { total, count, average, hourly };
  }, [transactions]);
  
  return (
    <div className="dashboard">
      <header>
        <h1>Real-Time Analytics</h1>
        <div className={`status ${connected ? 'online' : 'offline'}`}>
          {connected ? '🟢 Live' : '🔴 Offline'}
        </div>
      </header>
      
      <div className="metrics-grid">
        <MetricCard 
          title="Total Revenue" 
          value={`$${metrics.total.toLocaleString()}`}
        />
        <MetricCard 
          title="Transaction Count" 
          value={metrics.count}
        />
        <MetricCard 
          title="Average Transaction" 
          value={`$${metrics.average.toFixed(2)}`}
        />
      </div>
      
      {liveData && (
        <div className="live-update">
          New transaction: {liveData.product} - ${liveData.amount}
        </div>
      )}
      
      <TransactionTable transactions={transactions.slice(0, 20)} />
    </div>
  );
}

function MetricCard({ title, value }) {
  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <div className="value">{value}</div>
    </div>
  );
}

function TransactionTable({ transactions }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Amount</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map(t => (
          <tr key={t.id}>
            <td>{t.product}</td>
            <td>${t.amount}</td>
            <td>{new Date(t.timestamp).toLocaleTimeString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

---

## Essential Tooling

### Build Tools

**Vite** is the modern standard for React development:

```bash
# Create new React project
npm create vite@latest my-dashboard -- --template react

# Install dependencies
cd my-dashboard
npm install

# Start development server
npm run dev
```

Vite provides instant hot module reloading, making development fast.

### Helpful Libraries

For data-intensive apps, consider:

- **Chart.js / Recharts** - Data visualization
- **TanStack Query (React Query)** - Advanced data fetching/caching
- **Zustand** - Lightweight state management
- **date-fns** - Date manipulation
- **axios** - Enhanced HTTP client with interceptors

```bash
npm install recharts zustand date-fns axios
```

---

## Key Takeaways

1. **Master array methods** (`map`, `filter`, `reduce`) - you'll use them constantly
2. **Understand async/await** - all data fetching is asynchronous
3. **Use hooks properly** - `useState` for data, `useEffect` for side effects
4. **Optimize selectively** - `useMemo` and `memo` for expensive operations
5. **Handle real-time data** - WebSockets for live updates, polling for simplicity
6. **Build reusable patterns** - Custom hooks encapsulate complex logic

The beauty of modern JavaScript and React is that you can start simple and progressively add complexity as needed. Start with basic `useState` and `useEffect`, then layer in optimization and real-time features as your application grows.

Now you have the foundation to build sophisticated, performant data-intensive frontends. The key is practice—start with a simple dashboard and incrementally add features as you master each concept.
