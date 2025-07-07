import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { LocationService } from '../utils/LocationService';
import { WeatherService } from '../utils/WeatherService';
import { RecommendationsEngine } from '../utils/RecommendationsEngine';

export default function HomeScreen() {
  const [loading, setLoading] = useState(true);
  const [weather, setWeather] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const location = await LocationService.getCurrentLocation();
      const weatherData = await WeatherService.getWeatherData(
        location.coords.latitude,
        location.coords.longitude
      );

      setWeather(weatherData);
      
      const wateringRec = RecommendationsEngine.analyzeWateringNeeds(weatherData);
      const mowingRec = RecommendationsEngine.analyzeMowingConditions(weatherData);
      
      setRecommendations({ watering: wateringRec, mowing: mowingRec });
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    loadData().then(() => setRefreshing(false));
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.weatherCard}>
        <Text style={styles.title}>Current Weather</Text>
        <Text style={styles.weatherText}>
          Temperature: {weather.current.temp}°C
        </Text>
        <Text style={styles.weatherText}>
          Humidity: {weather.current.humidity}%
        </Text>
      </View>

      <View style={styles.recommendationCard}>
        <Text style={styles.title}>Recommendations</Text>
        <Text style={styles.recText}>
          Watering: {recommendations.watering.shouldWater ? 'Recommended' : 'Not Needed'}
        </Text>
        <Text style={styles.recReason}>{recommendations.watering.reason}</Text>
        
        <Text style={styles.recText}>
          Mowing: {recommendations.mowing.shouldMow ? 'Good conditions' : 'Not Recommended'}
        </Text>
        <Text style={styles.recReason}>{recommendations.mowing.reason}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  weatherCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    elevation: 2,
  },
  recommendationCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    elevation: 2,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  weatherText: {
    fontSize: 16,
    marginBottom: 4,
  },
  recText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 8,
  },
  recReason: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
});
