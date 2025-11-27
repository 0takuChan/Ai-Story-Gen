import React from 'react'
import './ChoiceButtons.css'

function ChoiceButtons({ choices, choiceEndings = [], onChoice, disabled }) {
  return (
    <div className="choice-buttons">
      <h3>เลือกการกระทำของคุณ:</h3>
      <div className="choices-grid">
        {choices.map((choice, index) => (
          <button
            key={index}
            className={`choice-button ${choiceEndings[index] ? 'ending-choice' : ''}`}
            onClick={() => onChoice(index, choice)}
            disabled={disabled}
          >
            <span className="choice-number">{index + 1}</span>
            <span className="choice-text">
              {choice}
              {choiceEndings[index]}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default ChoiceButtons
