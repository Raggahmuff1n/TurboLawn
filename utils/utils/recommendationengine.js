export class RecommendationsEngine {
  static analyzeWateringNeeds(weatherData, climateZone) {
    const recentRainfall = this.calculateRecentRainfall(weatherData);
    const upcomingRainfall = this.calculateUpcomingRainfall(weatherData);
    const temperature = weatherData.current.temp;
    const humidity = weatherData.current.humidity;

    // Basic logic for watering recommendations
    if (recentRainfall > 25) { // More than 25mm of rain in past 3 days
      return {
        shouldWater: false,
        reason: 'Recent rainfall sufficient'
      };
    }

    if (upcomingRainfall > 10) { // More than 10mm of rain expected
      return {
        shouldWater: false,
        reason: 'Rain expected soon'
      };
    }

    if (temperature > 30 && humidity < 40) { // Hot and dry conditions
      return {
        shouldWater: true,
        reason: 'Hot and dry conditions'
      };
    }

    return {
      shouldWater: true,
      reason: 'Regular watering schedule'
    };
  }

  static analyzeMowingConditions(weatherData) {
    const upcoming24h = weatherData.hourly.slice(0, 24);
    const hasRain = upcoming24h.some(hour => hour.rain);
    const maxTemp = Math.max(...upcoming24h.map(hour => hour.temp));

    if (hasRain) {
      return {
        shouldMow: false,
        reason: 'Rain expected'
      };
    }

    if (maxTemp > 35) {
      return {
        shouldMow: false,
        reason: 'Temperature too high'
      };
    }

    return {
      shouldMow: true,
      reason: 'Good conditions for mowing'
    };
  }

  static calculateRecentRainfall(weatherData) {
    return weatherData.daily
      .slice(0, 3)
      .reduce((total, day) => total + (day.rain || 0), 0);
  }

  static calculateUpcomingRainfall(weatherData) {
    return weatherData.daily
      .slice(0, 3)
      .reduce((total, day) => total + (day.rain || 0), 0);
  }
}
