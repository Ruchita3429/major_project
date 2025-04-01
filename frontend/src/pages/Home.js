import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Box,
} from '@mui/material';

const exercises = [
  {
    id: 'left-bicep',
    title: 'Left Bicep Curl',
    description: 'Practice your left arm bicep curls with real-time form correction.',
    image: '/assets/bicep.jpg',
  },
  {
    id: 'right-bicep',
    title: 'Right Bicep Curl',
    description: 'Practice your right arm bicep curls with real-time form correction.',
    image: '/assets/bicep.jpg',
  },
  {
    id: 'pushup',
    title: 'Push-ups',
    description: 'Perfect your push-up form with AI-powered guidance.',
    image: '/assets/pushup.png',
  },
  {
    id: 'squat',
    title: 'Squats',
    description: 'Master the squat technique with real-time feedback.',
    image: '/assets/squats.jpg',
  },
];

function Home() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome to GymJam
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Your AI-powered personal trainer for perfect form and technique
        </Typography>
      </Box>
      <Grid container spacing={4}>
        {exercises.map((exercise) => (
          <Grid item key={exercise.id} xs={12} sm={6} md={3}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardMedia
                component="img"
                height="200"
                image={exercise.image}
                alt={exercise.title}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="h2">
                  {exercise.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {exercise.description}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  onClick={() => navigate(`/exercise/${exercise.id}`)}
                >
                  Start Exercise
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default Home; 