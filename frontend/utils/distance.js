export default function distanceInMiles(lat1, lon1, lat2, lon2) {
  const earthRadiusInMiles = 3958.8;
  const degreesToRadians = Math.PI / 180;

  const lat1Radians = lat1 * degreesToRadians;
  const lon1Radians = lon1 * degreesToRadians;
  const lat2Radians = lat2 * degreesToRadians;
  const lon2Radians = lon2 * degreesToRadians;

  const deltaLat = lat2Radians - lat1Radians;
  const deltaLon = lon2Radians - lon1Radians;

  const a =
    Math.sin(deltaLat / 2) ** 2 +
    Math.cos(lat1Radians) * Math.cos(lat2Radians) * Math.sin(deltaLon / 2) ** 2;

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  const distanceInMiles = earthRadiusInMiles * c;

  return distanceInMiles.toFixed(0);
}
