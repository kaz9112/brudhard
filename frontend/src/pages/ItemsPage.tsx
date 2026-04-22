import React, { useState } from 'react';
import { useItems } from '../hooks/useItems';

const ItemsPage: React.FC = () => {
  const { items, addItem, loading } = useItems();
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim()) {
      addItem(title, desc);
      setTitle('');
      setDesc('');
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h2>Inventory Management</h2>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            placeholder="Item Title" 
            required
          />
          <input 
            value={desc} 
            onChange={(e) => setDesc(e.target.value)} 
            placeholder="Description" 
          />
          <button type="submit">Create</button>
        </div>
      </form>

      <hr />

      {loading ? (
        <p>Loading database items...</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {items.map((item) => (
            <li key={item.id} style={{ 
              padding: '10px', 
              borderBottom: '1px solid #eee',
              display: 'flex',
              justifyContent: 'space-between'
            }}>
              <span><strong>{item.title}</strong></span>
              <span style={{ color: '#666' }}>{item.description}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ItemsPage;