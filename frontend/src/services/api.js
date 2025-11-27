import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getThemes = async () => {
  const response = await api.get('/game/themes')
  return response.data
}

export const startGame = async (theme) => {
  const response = await api.post('/game/start', { theme })
  return response.data
}

export const makeAction = async (storyId, action) => {
  const response = await api.post('/game/action', {
    story_id: storyId,
    action: action,
  })
  return response.data
}

export default api
