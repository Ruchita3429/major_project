import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  OutlinedInput,
  Checkbox,
  ListItemText,
  Button,
  FormControlLabel,
  FormGroup,
  Slider,
  Grid,
  Alert,
} from '@mui/material';
import WorkoutPlan from '../components/WorkoutPlan';

const fitnessGoals = [
  'Flexibility',
  'Mind-Body Connection',
  'Cardiovascular Endurance'
];

const equipmentList = [
  'Jump Rope',
  'Yoga Blocks'
];

const experienceLevels = ['Beginner', 'Intermediate'];

const workoutTypes = [
  'Yoga',
  'Cardio'
];

const bodyParts = [
  'Full Body',
  'Core',
  'Upper Body',
  'Lower Body',
  'Back',
  'Shoulders'
];

function WorkoutGenerator() {
  const [formData, setFormData] = useState({
    fitnessGoal: 'Flexibility',
    equipment: [],
    duration: 30,
    experienceLevel: 'Beginner',
    workoutType: 'Yoga',
    bodyweightOnly: false,
    restrictions: [],
  });
  const [generatedWorkout, setGeneratedWorkout] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleMultiSelectChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: typeof value === 'string' ? value.split(',') : value,
    }));
  };

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: checked,
      // Clear equipment selection if bodyweight only is checked
      equipment: checked ? [] : prev.equipment,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/generate-workout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fitnessGoal: formData.fitnessGoal,
          availableEquipment: formData.bodyweightOnly ? ['Bodyweight Only'] : formData.equipment,
          duration: formData.duration,
          experienceLevel: formData.experienceLevel,
          workoutType: formData.workoutType,
          restrictions: formData.restrictions,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate workout');
      }

      const workout = await response.json();
      console.log('Generated workout:', workout);
      setGeneratedWorkout(workout);
    } catch (err) {
      setError(err.message || 'Failed to generate workout. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Smart Workout Generator
        </Typography>
        
        <Paper elevation={3} sx={{ p: 3 }}>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Fitness Goal</InputLabel>
                  <Select
                    name="fitnessGoal"
                    value={formData.fitnessGoal}
                    onChange={handleChange}
                    label="Fitness Goal"
                    required
                  >
                    {fitnessGoals.map((goal) => (
                      <MenuItem key={goal} value={goal}>
                        {goal}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Experience Level</InputLabel>
                  <Select
                    name="experienceLevel"
                    value={formData.experienceLevel}
                    onChange={handleChange}
                    label="Experience Level"
                    required
                  >
                    {experienceLevels.map((level) => (
                      <MenuItem key={level} value={level}>
                        {level}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Available Equipment</InputLabel>
                  <Select
                    multiple
                    name="equipment"
                    value={formData.equipment}
                    onChange={handleMultiSelectChange}
                    input={<OutlinedInput label="Available Equipment" />}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                          <Chip key={value} label={value} />
                        ))}
                      </Box>
                    )}
                    disabled={formData.bodyweightOnly}
                  >
                    {equipmentList.map((item) => (
                      <MenuItem key={item} value={item}>
                        <Checkbox checked={formData.equipment.indexOf(item) > -1} />
                        <ListItemText primary={item} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={formData.bodyweightOnly}
                      onChange={handleCheckboxChange}
                      name="bodyweightOnly"
                    />
                  }
                  label="Bodyweight Only"
                  sx={{ mt: 1 }}
                />
              </Grid>

              <Grid item xs={12}>
                <Typography gutterBottom>
                  Workout Duration (minutes): {formData.duration}
                </Typography>
                <Slider
                  name="duration"
                  value={formData.duration}
                  onChange={(e, newValue) =>
                    handleChange({ target: { name: 'duration', value: newValue } })
                  }
                  min={15}
                  max={60}
                  step={15}
                  marks={[
                    { value: 15, label: '15m' },
                    { value: 30, label: '30m' },
                    { value: 45, label: '45m' },
                    { value: 60, label: '1h' },
                  ]}
                />
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Workout Type</InputLabel>
                  <Select
                    name="workoutType"
                    value={formData.workoutType}
                    onChange={handleChange}
                    label="Workout Type"
                    required
                  >
                    {workoutTypes.map((type) => (
                      <MenuItem key={type} value={type}>
                        {type}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Restrictions/Injuries</InputLabel>
                  <Select
                    multiple
                    name="restrictions"
                    value={formData.restrictions}
                    onChange={handleMultiSelectChange}
                    input={<OutlinedInput label="Restrictions/Injuries" />}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                          <Chip key={value} label={value} />
                        ))}
                      </Box>
                    )}
                  >
                    {bodyParts.map((part) => (
                      <MenuItem key={part} value={part}>
                        <Checkbox checked={formData.restrictions.indexOf(part) > -1} />
                        <ListItemText primary={part} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ mt: 3 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    disabled={loading}
                  >
                    {loading ? 'Generating...' : 'Generate Workout'}
                  </Button>
                </Box>

                {error && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                  </Alert>
                )}
              </Grid>
            </Grid>
          </form>
        </Paper>

        {generatedWorkout && <WorkoutPlan workout={generatedWorkout} />}
      </Box>
    </Container>
  );
}

export default WorkoutGenerator; 