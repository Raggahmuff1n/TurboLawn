import * as Location from 'expo-location';
import AsyncStorage from '@react-native-async-storage/async-storage';

export class LocationService {
  static async getCurrentLocation() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        throw new Error('Permission to access location was denied');
      }

      const location = await Location.getCurrentPositionAsync({});
      return location;
    } catch (error) {
      console.error('Error getting location:', error);
      throw error;
    }
  }

  static async saveLocation(location) {
    try {
      const locations = await this.getSavedLocations();
      locations.push(location);
      await AsyncStorage.setItem('saved_locations', JSON.stringify(locations));
    } catch (error) {
      console.error('Error saving location:', error);
      throw error;
    }
  }

  static async getSavedLocations() {
    try {
      const locations = await AsyncStorage.getItem('saved_locations');
      return locations ? JSON.parse(locations) : [];
    } catch (error) {
      console.error('Error getting saved locations:', error);
      return [];
    }
  }
}
