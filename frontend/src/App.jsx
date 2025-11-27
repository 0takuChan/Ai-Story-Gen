import { useState, useEffect } from 'react'
import ThemeSelector from './components/ThemeSelector'
import StoryDisplay from './components/StoryDisplay'
import ChoiceButtons from './components/ChoiceButtons'
import { startGame, makeAction, getThemes } from './services/api'
import './App.css'

function App() {
  const [gameState, setGameState] = useState('theme-selection') // theme-selection, playing, ended
  const [themes, setThemes] = useState([])
  const [currentStory, setCurrentStory] = useState(null)
  const [storyHistory, setStoryHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [userInput, setUserInput] = useState('')

  useEffect(() => {
    loadThemes()
  }, [])

  const loadThemes = async () => {
    try {
      const data = await getThemes()
      setThemes(data.themes)
    } catch (error) {
      console.error('Error loading themes:', error)
    }
  }

  const handleStartGame = async (themeId) => {
    setLoading(true)
    try {
      const story = await startGame(themeId)
      setCurrentStory(story)
      setStoryHistory([{ 
        narrative: story.narrative, 
        directions: story.directions,
        objects: story.objects,
        hint: story.hint
      }])
      setGameState('playing')
    } catch (error) {
      console.error('Error starting game:', error)
      alert('ไม่สามารถเริ่มเกมได้ กรุณาลองใหม่อีกครั้ง')
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (actionText) => {
    if (!actionText.trim()) {
      alert('กรุณาพิมพ์การกระทำที่ต้องการ')
      return
    }

    setLoading(true)
    try {
      const nextStory = await makeAction(
        currentStory.story_id,
        actionText
      )
      
      setCurrentStory(nextStory)
      setStoryHistory([
        ...storyHistory,
        { 
          narrative: nextStory.narrative, 
          directions: nextStory.directions,
          objects: nextStory.objects,
          hint: nextStory.hint
        }
      ])
      setUserInput('') // ล้างช่องพิมพ์

      if (nextStory.is_ending) {
        setGameState('ended')
      }
    } catch (error) {
      console.error('Error making action:', error)
      alert('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง')
    } finally {
      setLoading(false)
    }
  }

  const handleRestart = () => {
    setGameState('theme-selection')
    setCurrentStory(null)
    setStoryHistory([])
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Adventure Story Game</h1>
        <p>สำรวจโลกและเลือกเส้นทางของคุณเอง</p>
      </header>

      <main className="app-main">
        {gameState === 'theme-selection' && (
          <ThemeSelector
            themes={themes}
            onSelectTheme={handleStartGame}
            loading={loading}
          />
        )}

        {(gameState === 'playing' || gameState === 'ended') && currentStory && (
          <div className="game-container">
            <StoryDisplay
              storyHistory={storyHistory}
              isEnding={gameState === 'ended'}
            />

            {gameState === 'playing' && (
              <div className="action-input-container">
                {/* แสดงกระเป๋า */}
                {currentStory.inventory && (
                  <div className="info-section inventory">
                    <p><strong>🎒 กระเป๋า:</strong> {currentStory.inventory.length > 0 ? currentStory.inventory.join(', ') : 'ว่างเปล่า'}</p>
                  </div>
                )}

                {/* แสดงทิศทางที่ไปได้ */}
                {currentStory.directions && currentStory.directions.length > 0 && (
                  <div className="info-section">
                    <p><strong>ทิศทางที่ไปได้:</strong> {currentStory.directions.join(', ')}</p>
                  </div>
                )}

                {/* แสดงสิ่งของที่สำรวจได้ */}
                {currentStory.objects && currentStory.objects.length > 0 && (
                  <div className="info-section">
                    <p><strong>สิ่งที่สำรวจได้:</strong> {currentStory.objects.join(', ')}</p>
                  </div>
                )}

                {/* แสดงคำแนะนำ */}
                {currentStory.hint && (
                  <div className="info-section hint">
                    <p><em>คำแนะนำ: {currentStory.hint}</em></p>
                  </div>
                )}

                {/* ช่องพิมพ์การกระทำเอง */}
                <div className="custom-action-section">
                  <p><strong>พิมพ์การกระทำของคุณ:</strong></p>
                  <div className="input-group">
                    <input
                      type="text"
                      value={userInput}
                      onChange={(e) => setUserInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleAction(userInput)}
                      placeholder="เช่น: เดินไปข้างหน้า, เปิดประตู, พูดคุยกับคนแปลกหน้า..."
                      disabled={loading}
                      className="action-input"
                    />
                    <button
                      onClick={() => handleAction(userInput)}
                      disabled={loading || !userInput.trim()}
                      className="submit-btn"
                    >
                      ส่ง
                    </button>
                  </div>
                </div>
              </div>
            )}

            {gameState === 'ended' && (
              <div className="game-end">
                <h2>จบเรื่อง</h2>
                <button onClick={handleRestart} className="restart-button">
                  เริ่มเกมใหม่
                </button>
              </div>
            )}

            {loading && (
              <div className="loading-overlay">
                <div className="loading-spinner">
                  <div className="spinner"></div>
                  <p>AI กำลังสร้างเรื่อง...</p>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
