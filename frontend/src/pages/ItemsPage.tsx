import React, { useState } from 'react';
import { useItems } from '../hooks/useItems';

const ItemsPage: React.FC = () => {
  const { items, addItem, loading } = useItems();
  const [title, setTitle] = useState('');
  const [fileContent, setFileContent] = useState('');

  // Function to handle the .txt file upload and conversion to string
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    
    if (file && file.type === "text/plain") {
      const reader = new FileReader();
      
      reader.onload = (event) => {
        const text = event.target?.result;
        setFileContent(text as string);
      };

      reader.onerror = () => {
        console.error("Failed to read file");
      };

      reader.readAsText(file);
    } else {
      alert("Please upload a valid .txt file");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim() && fileContent) {
      // Passing title and the file content string to your hook
      addItem(title, fileContent);
      
      // Resetting state
      setTitle('');
      setFileContent('');
      // Note: To clear the file input UI, you'd need a ref, 
      // but the state is now cleared for the next submission.
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h2>Inventory Management</h2>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <input 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            placeholder="Item Title" 
            required
          />
          
          <label style={{ fontSize: '14px', color: '#555' }}>
            Upload .txt file for description:
            <input 
              type="file" 
              accept=".txt" 
              onChange={handleFileUpload} 
              style={{ display: 'block', marginTop: '5px' }}
              required
            />
          </label>

          <button type="submit" disabled={!fileContent}>Create</button>
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
              flexDirection: 'column'
            }}>
              <span><strong>{item.title}</strong></span>
              <p style={{ color: '#666', fontSize: '13px', margin: '5px 0 0' }}>
                {item.description}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ItemsPage;