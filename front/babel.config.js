module.exports = function (api) {
  api.cache(true);
  return {
    // babel-preset-expo also adds the react-native-worklets plugin used by Reanimated 4
    presets: ['babel-preset-expo'],
  };
};
