import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import Timer from '../components/Timer';
import socketService from '../services/socketService';

const exerciseEndpoints = {
  'left-bicep': '/video_feed_left',
  'right-bicep': '/video_feed_right',
  'pushup': '/video_feed_pushup',
  'squat': '/video_feed_squat',
  'sun-salutation': '/video_feed_sun_salutation',
  'mountain-climbers': '/video_feed_mountain_climbers',
  'jump-rope': '/video_feed_jump_rope',
  'yoga-blocks': '/video_feed_yoga_blocks'
};

const exerciseInstructions = {
  'left-bicep': {
    description: 'Keep your back straight and curl your left arm up towards your shoulder.',
    tips: [
      'Keep your elbow close to your body',
      'Maintain a controlled movement',
      'Avoid swinging or using momentum',
      'Keep your wrist straight',
      'Breathe out as you curl up',
    ],
    commonMistakes: [
      'Swinging the arm',
      'Moving the elbow away from the body',
      'Using momentum instead of muscle control',
      'Arching the back',
    ],
  },
  'right-bicep': {
    description: 'Keep your back straight and curl your right arm up towards your shoulder.',
    tips: [
      'Keep your elbow close to your body',
      'Maintain a controlled movement',
      'Avoid swinging or using momentum',
      'Keep your wrist straight',
      'Breathe out as you curl up',
    ],
    commonMistakes: [
      'Swinging the arm',
      'Moving the elbow away from the body',
      'Using momentum instead of muscle control',
      'Arching the back',
    ],
  },
  'pushup': {
    description: 'Keep your body straight and lower your chest towards the ground.',
    tips: [
      'Keep your body in a straight line',
      'Hands shoulder-width apart',
      'Elbows close to your body',
      'Lower until your chest nearly touches the ground',
      'Push back up explosively',
    ],
    commonMistakes: [
      'Sagging hips',
      'Flaring elbows',
      'Not going low enough',
      'Moving too quickly',
    ],
  },
  'squat': {
    description: 'Keep your back straight and lower your body as if sitting back into a chair.',
    tips: [
      'Keep your back straight',
      'Knees aligned with toes',
      'Lower until thighs are parallel to ground',
      'Keep weight in your heels',
      'Breathe out as you stand up',
    ],
    commonMistakes: [
      'Knees caving inward',
      'Rounding the back',
      'Not going low enough',
      'Lifting heels off the ground',
    ],
  },
  'sun-salutation': {
    description: 'A flowing sequence of yoga poses that serves as a warm-up or complete practice.',
    tips: [
      'Move with your breath',
      'Keep your core engaged throughout the sequence',
      'Focus on alignment in each pose',
      'Move slowly and mindfully',
      'Modify poses as needed for your body'
    ],
    commonMistakes: [
      'Rushing through the sequence',
      'Holding the breath',
      'Rounding the back in forward folds',
      'Collapsing in plank pose'
    ]
  },
  'mountain-climbers': {
    description: 'Starting in a plank position, alternately bring knees to chest in a running motion.',
    tips: [
      'Keep your core tight',
      'Maintain a straight line from head to heels',
      'Move at a controlled pace',
      'Keep shoulders over wrists',
      'Land lightly on your toes'
    ],
    commonMistakes: [
      'Sagging hips',
      'Moving too slowly',
      'Bouncing up and down',
      'Not bringing knees close enough to chest'
    ]
  },
  'jump-rope': {
    description: 'Jump over a rope as it passes under your feet, swung by your hands.',
    tips: [
      'Keep elbows close to body',
      'Jump just high enough to clear the rope',
      'Land softly on the balls of your feet',
      'Maintain a steady rhythm',
      'Keep your core engaged'
    ],
    commonMistakes: [
      'Jumping too high',
      'Arms too far from body',
      'Landing flat-footed',
      'Inconsistent pace'
    ]
  },
  'yoga-blocks': {
    description: 'Use yoga blocks to support and enhance various yoga poses.',
    tips: [
      'Use blocks to maintain proper alignment',
      'Keep spine long and engaged',
      'Breathe deeply and steadily',
      'Place blocks securely on the ground',
      'Modify block height as needed'
    ],
    commonMistakes: [
      'Placing blocks unstably',
      'Collapsing weight into the blocks',
      'Holding the breath',
      'Improper block height for your flexibility'
    ]
  }
};

function Exercise() {
  const { type } = useParams();
  const navigate = useNavigate();
  const [count, setCount] = useState(0);
  const [status, setStatus] = useState('Ready to start');
  const [currentSet, setCurrentSet] = useState(1);
  const [isResting, setIsResting] = useState(false);
  const [formTips, setFormTips] = useState([]);

  useEffect(() => {
    if (!exerciseEndpoints[type]) return;

    socketService.subscribeToExerciseUpdates(type, {
      onUpdate: (data) => {
        setFormTips(data.formTips || []);
      },
      onCount: (data) => {
        setCount(data.count);
      },
      onStatus: (data) => {
        setStatus(data.status);
      },
    });

    return () => {
      socketService.unsubscribeFromExerciseUpdates();
    };
  }, [type]);

  const handleWorkoutComplete = () => {
    setIsResting(true);
    setStatus('Rest Period');
  };

  const handleRestComplete = () => {
    setIsResting(false);
    setCurrentSet(prev => prev + 1);
    setStatus('Ready for next set');
  };

  if (!exerciseEndpoints[type]) {
    return (
      <Container>
        <Typography variant="h4" color="error">
          Exercise not found
        </Typography>
      </Container>
    );
  }

  const exercise = exerciseInstructions[type];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          sx={{ mb: 2 }}
        >
          Back to Exercises
        </Button>
        <Typography variant="h4" component="h1" gutterBottom>
          {type.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              height: '600px',
              overflow: 'hidden',
            }}
          >
            <img
              src={window.location.origin + exerciseEndpoints[type]}
              alt="Exercise Feed"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
              }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Exercise Instructions
            </Typography>
            <Typography paragraph>
              {exercise.description}
            </Typography>

            <Divider sx={{ my: 2 }} />

            <Typography variant="h6" gutterBottom>
              Form Tips
            </Typography>
            <List>
              {exercise.tips.map((tip, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={tip} />
                </ListItem>
              ))}
            </List>

            <Divider sx={{ my: 2 }} />

            <Typography variant="h6" gutterBottom>
              Common Mistakes
            </Typography>
            <List>
              {exercise.commonMistakes.map((mistake, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <WarningIcon color="error" />
                  </ListItemIcon>
                  <ListItemText primary={mistake} />
                </ListItem>
              ))}
            </List>

            <Divider sx={{ my: 2 }} />

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" gutterBottom>
                Set {currentSet}
              </Typography>
              <Typography variant="h3" color="primary">
                {count}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Reps Completed
              </Typography>
              <Typography
                variant="body1"
                color={status === 'Ready to start' ? 'text.secondary' : 'primary'}
                gutterBottom
              >
                Status: {status}
              </Typography>

              {formTips.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" color="error">
                    Form Corrections:
                  </Typography>
                  <List>
                    {formTips.map((tip, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <WarningIcon color="error" />
                        </ListItemIcon>
                        <ListItemText primary={tip} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              <Box sx={{ mt: 2 }}>
                <Timer
                  duration={isResting ? 60 : 180}
                  onComplete={isResting ? handleRestComplete : handleWorkoutComplete}
                  isRest={isResting}
                />
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Exercise; 