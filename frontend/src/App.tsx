import ItemsPage from './pages/ItemsPage';

function App() {
  return (
    <div className="App">
      {/* You can add a Header or Navbar here later */}
      <nav style={{ padding: '1rem', background: '#282c34', color: 'white' }}>
        <strong>FastAPI + React Demo</strong>
      </nav>

      <main>
        <ItemsPage />
      </main>
    </div>
  );
}

export default App;