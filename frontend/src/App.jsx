import { useState } from 'react'
import './App.css'
import Calendar from './Calendar'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Oh-Brother (오늘의 교회)</h1>
      </header>
      <main>
        <Calendar />
      </main>
    </div>
  )
}

export default App
