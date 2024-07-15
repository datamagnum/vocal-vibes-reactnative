/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
	presets: ['module:@react-native/babel-preset', 'nativewind/babel'],
	env: {
		production: {
			plugins: ['react-native-paper/babel'],
		},
	},
	plugins: [
		[
			'module-resolver',
			{
				root: ['./src'],
				extensions: ['.js', '.json', '.css','.tsx','.ts'],
				alias: {
					'@': './src',
				},
			},
		],
		'inline-dotenv',
		'react-native-reanimated/plugin', // needs to be last
	],
};
