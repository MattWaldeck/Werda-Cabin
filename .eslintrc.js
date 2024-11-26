module.exports = {
  extends: ['airbnb', 'airbnb-typescript'],
  parserOptions: {
    project: './tsconfig.json',
  },
  rules: {
    // Add or override rules here
    'react/react-in-jsx-scope': 'off', // if using React 17+
    'import/prefer-default-export': 'off',
  },
};
