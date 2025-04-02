import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
  Button,
  Grid,
  Stack,
  Alert,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import TimerIcon from '@mui/icons-material/Timer';
import RepeatIcon from '@mui/icons-material/Repeat';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import TargetIcon from '@mui/icons-material/TrackChanges';
import InfoIcon from '@mui/icons-material/Info';

// Map exercise names to their endpoint routes
const exerciseRouteMap = {
  'Push-ups': 'pushup',
  'Squats': 'squat',
  'Dumbbell Row': 'dumbbell-row',
  'Sun Salutation': 'sun-salutation',
  'Mountain Climbers': 'mountain-climbers',
  'Jump Rope': 'jump-rope',
  'Yoga with Blocks': 'yoga-blocks'
};

function WorkoutPlan({ workout }) {
  const navigate = useNavigate();
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);

  if (!workout) return null;
  if (!workout.exercises || workout.exercises.length === 0) {
    return (
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Alert severity="warning">
          No exercises found in the workout plan. Please try generating a new workout.
        </Alert>
      </Paper>
    );
  }

  const handleStartExercise = (exerciseName) => {
    if (!exerciseName) {
      console.error('Exercise name is undefined');
      return;
    }
    const exerciseRoute = exerciseRouteMap[exerciseName];
    if (!exerciseRoute) {
      console.error(`No route mapping found for exercise: ${exerciseName}`);
      return;
    }
    navigate(`/exercise/${exerciseRoute}`);
  };

  const handleStartWorkout = () => {
    if (workout.exercises && workout.exercises.length > 0) {
      const firstExercise = workout.exercises[0];
      if (firstExercise && firstExercise.name) {
        handleStartExercise(firstExercise.name);
      } else {
        console.error('First exercise is invalid:', firstExercise);
      }
    } else {
      console.error('No valid exercises found in the workout');
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mt: 4, bgcolor: 'background.paper' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom color="primary">
          Your Custom Workout Plan
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          {workout.description}
        </Typography>
        <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
          <Chip
            icon={<TimerIcon />}
            label={`${workout.duration} minutes`}
            color="primary"
            variant="outlined"
          />
          <Chip
            icon={<FitnessCenterIcon />}
            label={workout.type}
            color="secondary"
            variant="outlined"
          />
        </Stack>
      </Box>

      <Divider sx={{ my: 3 }} />

      {workout.exercises.map((exercise, index) => (
        exercise && exercise.name ? (
          <Accordion 
            key={index}
            expanded={selectedExercise === index}
            onChange={() => setSelectedExercise(selectedExercise === index ? null : index)}
            sx={{ mb: 2, bgcolor: 'background.default' }}
          >
            <AccordionSummary 
              expandIcon={<ExpandMoreIcon />}
              sx={{ '&:hover': { bgcolor: 'action.hover' } }}
            >
              <Grid container alignItems="center" spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="h6" color="primary">
                    {exercise.name}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Stack direction="row" spacing={1}>
                    <Chip
                      size="small"
                      icon={<RepeatIcon />}
                      label={`${exercise.sets} sets × ${exercise.reps} ${typeof exercise.reps === 'number' ? 'reps' : ''}`}
                      color="primary"
                      variant="outlined"
                    />
                    <Chip
                      size="small"
                      icon={<AccessTimeIcon />}
                      label={`${exercise.rest}s rest`}
                      color="secondary"
                      variant="outlined"
                    />
                  </Stack>
                </Grid>
              </Grid>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ p: 2 }}>
                <Stack spacing={2}>
                  <Box>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      <TargetIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Target Muscles:
                    </Typography>
                    <Typography variant="body2">
                      {exercise.targetMuscle}
                    </Typography>
                  </Box>

                  <Box>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      <InfoIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Instructions:
                    </Typography>
                    <Typography variant="body2" paragraph>
                      {exercise.instructions}
                    </Typography>
                  </Box>

                  {exercise.equipment && exercise.equipment !== 'None' && (
                    <Box>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        <FitnessCenterIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                        Equipment Needed:
                      </Typography>
                      <Typography variant="body2">
                        {exercise.equipment}
                      </Typography>
                    </Box>
                  )}

                  {exercise.formTips && exercise.formTips.length > 0 && (
                    <Box>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        Form Tips:
                      </Typography>
                      <List dense>
                        {exercise.formTips.map((tip, tipIndex) => (
                          <ListItem key={tipIndex}>
                            <ListItemText
                              primary={tip}
                              primaryTypographyProps={{
                                variant: 'body2',
                                color: 'text.secondary',
                              }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}

                  <Box sx={{ mt: 2 }}>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleStartExercise(exercise.name)}
                      fullWidth
                    >
                      Start {exercise.name}
                    </Button>
                  </Box>
                </Stack>
              </Box>
            </AccordionDetails>
          </Accordion>
        ) : null
      ))}

      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={handleStartWorkout}
        >
          Start Workout
        </Button>
        <Button
          variant="outlined"
          color="primary"
          size="large"
        >
          Save Workout
        </Button>
      </Box>
    </Paper>
  );
}

export default WorkoutPlan; 