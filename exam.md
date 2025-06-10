---
title: Changelog
description: All notable changes to this project
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### 🚀 Features

- **test commit v1.3.0** ([e398db7a](https://github.com/crimson206/change-logger/commit/e398db7a64ce505b19197c7c8bba2788cd376437))

- **I am so tired2** ([22a13ece](https://github.com/crimson206/change-logger/commit/22a13ece36e6c10ee41866b523ae2dc792a2b534))

- **I am so tired** ([7873c268](https://github.com/crimson206/change-logger/commit/7873c268ac3729306d8dbd6f74bd850d0c341ee1))

- **example feat message2** ([89adf217](https://github.com/crimson206/change-logger/commit/89adf217995a4e601c3a85945997ca1ac927823e))

- **example feat message** ([ebf31041](https://github.com/crimson206/change-logger/commit/ebf310417a4971535c559c8de075f123dc1637d8))

- **any message with correct syntax** ([0ba7df77](https://github.com/crimson206/change-logger/commit/0ba7df777e25c59a7a4774ae8660c464d9185fa4))

- **add comprehensive test suite and CI/CD pipeline** ([53229104](https://github.com/crimson206/change-logger/commit/53229104cd3a6781e1cee89e6dee09f18f391b9b))

  <details>
  <summary>📝 Details</summary>
  
  This commit establishes a robust testing and automation foundation:
  
  - Add unit tests for core functionality
  - Configure GitHub Actions for automated testing  
  - Set up semantic-release for automated versioning
  - Ensure code quality with linting and formatting checks
  
  The CI/CD pipeline now runs tests, validates code quality, and automatically generates releases with changelogs.
  
  Closes #CI-001
  
  </details>

- **improve error handling** ([4ef3b8eb](https://github.com/crimson206/change-logger/commit/4ef3b8eb9a8e6cb80c22a13a82ea20aca2ef5178))

### 🐛 Bug Fixes

- **resolve memory leak in data processing** ([a83f73cf](https://github.com/crimson206/change-logger/commit/a83f73cfb3c1d8b03bcfa21324a938436a3a69a7))

  <details>
  <summary>📝 Details</summary>
  
  The previous implementation had a memory leak when processing large datasets. This fix:
  
  - Properly closes database connections
  - Implements connection pooling  
  - Adds memory usage monitoring
  - Improves overall performance by 40%
  
  Fixes #MEM-456
  
  </details>

---

## v1.1.0 <small>(2025-06-10)</small> {#v1-1-0}

### 🚀 Features

- **implement user authentication system** ([f95830d](https://github.com/crimson206/change-logger/commit/f95830d9f6c50cbbc901b4101d19a06709ba0292))

  <details>
  <summary>📝 Details</summary>
  
  - Add JWT token generation and validation
  - Implement login/logout endpoints
  - Add password hashing with bcrypt
  - Create user session management
  - Add authentication middleware
  - Include comprehensive error handling
  - Add unit tests for auth functions
  
  Closes #123, #124, #125
  
  </details>

---

## v1.0.0 <small>(2025-06-10)</small> {#v1-0-0}

### 🚀 Features

- **initial package setup** ([81da6e4](https://github.com/crimson206/change-logger/commit/81da6e4c1e27e9abe60b11d76f38b7f99a3b1bb2))

  <details>
  <summary>📝 Details</summary>
  
  - Add basic package structure
  - Configure semantic release
  - Set up testing framework
  
  </details>

---

## v0.2.0 <small>(2025-06-10)</small> {#v0-2-0}

:::info
This version contains commits that don't follow conventional commit format.
:::

---

## v0.1.0 <small>(2025-06-10)</small> {#v0-1-0}

:::info
This version contains commits that don't follow conventional commit format.
:::

---

## Compare Versions

- [Unreleased Changes](https://github.com/crimson206/change-logger/compare/1.1.0...HEAD)
- [v1.1.0...v1.0.0](https://github.com/crimson206/change-logger/compare/1.0.0...1.1.0)
- [v1.0.0...v0.2.0](https://github.com/crimson206/change-logger/compare/0.2.0...1.0.0)
- [v0.2.0...v0.1.0](https://github.com/crimson206/change-logger/compare/0.1.0...0.2.0)

---

:::tip 💡 Tip
Click on commit hashes to view the full changes on GitHub, or expand the "Details" sections to see more information about each change.
:::