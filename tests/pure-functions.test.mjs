import { test } from 'node:test';
import assert from 'node:assert/strict';
import { timingSafeEqual, safeNum, nestedNum, formatDelta } from '../src/index.ts';

test('timingSafeEqual: identical strings match', () => {
  assert.equal(timingSafeEqual('a-real-secret-key', 'a-real-secret-key'), true);
});

test('timingSafeEqual: different values of equal length do not match', () => {
  assert.equal(timingSafeEqual('a-real-secret-key', 'a-fake-secret-key'), false);
});

test('timingSafeEqual: different-length values do not match', () => {
  assert.equal(timingSafeEqual('short', 'a-much-longer-value'), false);
});

test('timingSafeEqual: case-sensitive', () => {
  assert.equal(timingSafeEqual('Secret', 'secret'), false);
});

test('safeNum: passes through a real number', () => {
  assert.equal(safeNum(42), 42);
});

test('safeNum: parses a numeric string', () => {
  assert.equal(safeNum('3.14'), 3.14);
});

test('safeNum: falls back on a non-numeric string', () => {
  assert.equal(safeNum('not-a-number', -1), -1);
});

test('safeNum: falls back on null/undefined/objects', () => {
  assert.equal(safeNum(null), 0);
  assert.equal(safeNum(undefined, 7), 7);
  assert.equal(safeNum({}), 0);
});

test('nestedNum: walks a nested path', () => {
  assert.equal(nestedNum({ a: { b: { c: 5 } } }, 'a', 'b', 'c'), 5);
});

test('nestedNum: returns 0 for a missing path', () => {
  assert.equal(nestedNum({ a: {} }, 'a', 'b', 'c'), 0);
});

test('nestedNum: returns 0 when the path hits a non-object', () => {
  assert.equal(nestedNum({ a: 5 }, 'a', 'b'), 0);
});

test('formatDelta: zero diff renders as "0"', () => {
  assert.equal(formatDelta(10, 10), '0');
});

test('formatDelta: positive diff gets a plus sign and locale formatting', () => {
  assert.equal(formatDelta(1500, 500), '+1,000');
});

test('formatDelta: negative diff keeps its sign, no extra plus', () => {
  assert.equal(formatDelta(500, 1500), '-1,000');
});
