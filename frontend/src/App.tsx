import React, { useState } from 'react';
import { useItems } from './hooks/useItems';

function App() {
  const { items, addItem, loading } = useItems();
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title) {
      addItem(title, desc);
      setTitle('');
      setDesc('');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>FastAPI + React CRUD</h1>
      
      <form onSubmit={handleSubmit}>
        <input 
          value={title} 
          onChange={(e) => setTitle(e.target.value)} 
          placeholder="Title" 
        />
        <input 
          value={desc} 
          onChange={(e) => setDesc(e.target.value)} 
          placeholder="Description" 
        />
        <button type="submit">Add Item</button>
      </form>

      {loading ? <p>Loading...</p> : (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <strong>{item.title}</strong>: {item.description}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;