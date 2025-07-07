import AsyncStorage from '@react-native-async-storage/async-storage';

const API_KEY = 'YOUR_OPENWEATHER_API_KEY'; // Replace with actual API key

export class WeatherService {
  static async getWeatherData(latitude, longitude) {
    try {
      const cachedData = await this.getCachedWeatherData();
      if (cachedData && this.isCacheValid(cachedData.timestamp)) {
        return cachedData.data;
      }

      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/onecall?lat=${latitude}&lon=${longitude}&exclude=minutely&appid=${API_KEY}&units=metric`
      );
      const data = await response.json();
      
      await this.cacheWeatherData(data);
      return data;
    } catch (error) {
      console.error('Error fetching weather data:', error);
      throw error;
    }
  }

  static async cacheWeatherData(data) {
    try {
      await AsyncStorage.setItem('weather_cache', JSON.stringify({
        data,
        timestamp: new Date().getTime()
      }));
    } catch (error) {
      console.error('Error caching weather data:', error);
    }
  }

  static async getCachedWeatherData() {
    try {
      const cache = await AsyncStorage.getItem('weather_cache');
      return cache ? JSON.parse(cache) : null;
    } catch (error) {
      console.error('Error reading cached weather data:', error);
      return null;
    }
  }

  static isCacheValid(timestamp) {
    const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes
    return (new Date().getTime() - timestamp) < CACHE_DURATION;
  }
}
