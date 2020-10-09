import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';

export default [
	/* Main */
	{
		input: '_lib/js/pages/config/index.js',
		output: {
			file: 'webserver/src/js/config.js',
			format: 'iife',
			name: 'pg_config',
			sourcemap: false,
		},
		plugins: [
			babel({
				exclude: 'node_modules/**'
			}),
			resolve(),
		],
	},
];