import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Exercise from './pages/Exercise';
import WorkoutGenerator from './pages/WorkoutGenerator';
import FitnessCoach from './pages/FitnessCoach';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff4d4d',
    },
    secondary: {
      main: '#4d4dff',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/exercise/:type" element={<Exercise />} />
              <Route path="/workout-generator" element={<WorkoutGenerator />} />
              <Route path="/fitness-coach" element={<FitnessCoach />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App; 