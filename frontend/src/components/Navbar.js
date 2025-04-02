import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <FitnessCenterIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          GymJam
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            color="inherit"
            component={RouterLink}
            to="/"
          >
            Home
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/workout-generator"
            startIcon={<AutoAwesomeIcon />}
          >
            Workout Generator
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar; 