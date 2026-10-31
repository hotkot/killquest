'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const resolve = require('../desktop/asset-path.cjs');
const root = path.resolve('dist');
assert.equal(resolve(root, 'killquest://game/'), path.join(root, 'index.html'));
assert.equal(resolve(root, 'killquest://game/assets/phaser.min.js?v=1'), path.join(root, 'assets/phaser.min.js'));
for (const url of ['https://game/index.html', 'killquest://other/index.html',
  'killquest://game/%2e%2e%2fsecret', 'killquest://game/%5csecret',
  'killquest://game/%00', 'killquest://game/%zz']) assert.equal(resolve(root, url), null, url);
console.log('PASS desktop protocol: local assets, query stamps, rejected external/traversal/malformed paths.');
