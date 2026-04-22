import { useState, useEffect } from 'react';
import api from '../api/axios';

// Define the shape of our Item based on the backend model
export interface Item {
  id?: number;
  title: string;
  description: string | null;
}

export const useItems = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchItems = async () => {
    try {
      const response = await api.get<Item[]>('/items');
      setItems(response.data);
    } catch (error) {
      console.error("Error fetching items:", error);
    } finally {
      setLoading(false);
    }
  };

  const addItem = async (title: string, description: string) => {
    try {
      const response = await api.post<Item>('/items', { title, description });
      setItems((prev) => [...prev, response.data]);
    } catch (error) {
      console.error("Error adding item:", error);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return { items, addItem, loading };
};