import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Paper, 
  CircularProgress,
  Container,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  Alert,
  Snackbar
} from '@mui/material';
import { Send as SendIcon, SportsKabaddi as CoachIcon, Person as UserIcon } from '@mui/icons-material';

// API key for Gemini free tier
const GEMINI_API_KEY = 'AIzaSyDCxUJClzvXrYptO9BryDYYArw1u1c2wnU';

const FitnessCoach = () => {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: 'Hello! I\'m your AI Fitness Coach. Ask me any questions about workouts, nutrition, or fitness goals!' 
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleCloseError = () => {
    setError(null);
  };

  const sendMessage = async () => {
    if (input.trim() === '') return;
    
    // Add user message
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    
    try {
      // Using the free tier API key with optimized parameters
      const response = await fetch('https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': GEMINI_API_KEY
        },
        body: JSON.stringify({
          contents: [
            {
              role: 'user',
              parts: [
                {
                  text: `You are a professional fitness coach. Keep your answers concise and focused on fitness topics only. Answer the following question about fitness, nutrition, workouts, or wellness: ${input}`
                }
              ]
            }
          ],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 800, // Reduced token count for free tier
          },
          safetySettings: [
            {
              category: "HARM_CATEGORY_HARASSMENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_HATE_SPEECH",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_DANGEROUS_CONTENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            }
          ]
        })
      });
      
      const data = await response.json();
      
      if (data.candidates && data.candidates.length > 0) {
        const assistantMessage = { 
          role: 'assistant', 
          content: data.candidates[0].content.parts[0].text 
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else if (data.error) {
        // Handle specific API errors
        console.error('API Error:', data.error);
        setError(`API Error: ${data.error.message || 'Unknown error'}`);
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: `I encountered an error: ${data.error.message || 'Unknown error'}. This might be due to free tier API limitations. Please try again with a simpler question.` 
        }]);
      } else {
        throw new Error('No response from API');
      }
    } catch (error) {
      console.error('Error calling Gemini API:', error);
      setError(`Network Error: ${error.message}`);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I had trouble connecting to the fitness knowledge base. This might be due to free tier API limitations. Please try again in a moment.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom sx={{ mt: 2 }}>
        AI Fitness Coach
      </Typography>
      <Paper elevation={3} sx={{ height: '70vh', display: 'flex', flexDirection: 'column', mb: 2 }}>
        <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
          <List>
            {messages.map((message, index) => (
              <React.Fragment key={index}>
                <ListItem alignItems="flex-start" sx={{ 
                  justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                  mb: 1
                }}>
                  {message.role === 'assistant' && (
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        <CoachIcon />
                      </Avatar>
                    </ListItemAvatar>
                  )}
                  <ListItemText
                    primary={message.role === 'user' ? 'You' : 'Fitness Coach'}
                    secondary={
                      <Typography
                        component="span"
                        variant="body2"
                        color="text.primary"
                        sx={{ 
                          display: 'inline',
                          whiteSpace: 'pre-wrap'
                        }}
                      >
                        {message.content}
                      </Typography>
                    }
                    sx={{
                      backgroundColor: message.role === 'user' ? 'primary.dark' : 'background.paper',
                      borderRadius: 2,
                      p: 1,
                      maxWidth: '80%'
                    }}
                  />
                  {message.role === 'user' && (
                    <ListItemAvatar sx={{ ml: 1 }}>
                      <Avatar>
                        <UserIcon />
                      </Avatar>
                    </ListItemAvatar>
                  )}
                </ListItem>
                {index < messages.length - 1 && <Divider variant="inset" component="li" />}
              </React.Fragment>
            ))}
          </List>
          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
              <CircularProgress />
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>
        <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
            Using Gemini Free Tier API - Please keep questions brief and fitness-related
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TextField
              fullWidth
              multiline
              maxRows={3}
              variant="outlined"
              placeholder="Ask about workouts, nutrition, or fitness tips..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <Button 
              variant="contained" 
              color="primary" 
              endIcon={<SendIcon />}
              onClick={sendMessage}
              disabled={loading || input.trim() === ''}
              sx={{ ml: 1, height: 56 }}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>
      <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseError}>
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default FitnessCoach; 