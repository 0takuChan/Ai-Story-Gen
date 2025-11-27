import React from 'react'
import './StoryDisplay.css'

function StoryDisplay({ storyHistory, isEnding }) {
  return (
    <div className="story-display">
      <div className="story-content">
        {storyHistory.map((segment, index) => (
          <div key={index} className="story-segment">
            <p className="narrative">{segment.narrative}</p>
            {index < storyHistory.length - 1 && (
              <div className="divider">• • •</div>
            )}
          </div>
        ))}
      </div>
      {isEnding && (
        <div className="ending-badge">
          THE END 
        </div>
      )}
    </div>
  )
}

export default StoryDisplay
