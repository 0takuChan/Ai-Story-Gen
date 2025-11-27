import React from 'react'
import './ThemeSelector.css'

function ThemeSelector({ themes, onSelectTheme, loading }) {
  const getThemeEmoji = (themeId) => {
    const emojiMap = {
      adventure: '⚔️',
      mystery: '🔍',
      scifi: '🚀',
      horror: '👻',
      romance: '💖',
      fantasy: '🧙‍♂️',
      drama: '🎭',
    }
    return emojiMap[themeId] || '📖'
  }

  return (
    <div className="theme-selector">
      <h2>เลือกธีมเรื่องราว</h2>
      <div className="theme-grid">
        {themes.map((theme) => (
          <button
            key={theme.id}
            className="theme-card"
            onClick={() => onSelectTheme(theme.id)}
            disabled={loading}
          >
            <div className="theme-emoji">{getThemeEmoji(theme.id)}</div>
            <h3>{theme.name}</h3>
            <p>{theme.description}</p>
          </button>
        ))}
      </div>
    </div>
  )
}

export default ThemeSelector
