# Substrate Core Specification
Symantyx · Substrate Layer

## Purpose
Defines the foundational kernel logic, binding rules, and shim behavior for all Symantyx modules.

## Components

### 1. SubstrateCore
- Maintains registry of bound modules
- Provides substrate-level invariants
- Handles packet ingress/egress

### 2. EngineBind
- Binds engine modules to substrate
- Ensures hydration → collapse → bind → emit pipeline integrity

### 3. ContainerShim
- Wraps operators for safe execution
- Provides membrane-safe dispatch

## Invariants
- Substrate MUST remain domain-agnostic
- Substrate MUST support dynamic extension
- Substrate MUST preserve telos integrity
