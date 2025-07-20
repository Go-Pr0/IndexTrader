# Product Requirements Document: Non-Custodial Index Trading Platform

## Introduction

**The Problem:** Traders who analyze macro crypto trends, like the shifting dominance of Bitcoin (BTC.D), have no direct way to act on their insights. To take a position on a non-tradable metric like BTC.D, a trader must manually execute a complex series of trades across multiple assets (e.g., selling a basket of altcoins to buy BTC). This process is slow, error-prone, and difficult to manage, preventing traders from efficiently speculating on or hedging against broad market movements.

**Our Solution:** We are building a non-custodial platform that allows users to trade synthetic indices with a single click, using their own Bybit exchange account. Users securely connect their account via an API key. When a user decides to "buy" BTC.D, our platform automatically executes the underlying multi-leg **1x leverage futures trades** on their Bybit account to create a position that mirrors the index. The platform handles the complexity of order execution and position tracking, providing a simple interface to manage a sophisticated strategy. **At no point does our platform take custody of user funds.**

**Vision:** Our vision is to be the premier interface for non-custodial index trading. We will empower traders to leverage their own exchange accounts to seamlessly trade a variety of synthetic indices, from market dominance to sector-specific baskets (e.g., DeFi, Gaming). We will provide the simplest, most secure way to translate high-level market analysis into real-world trades without ever having to give up control of your assets.

## Goals and Objectives

**Business Goals:**
*   Achieve a target monthly active user base within six months of launch.
*   Establish a trusted brand identity in the non-custodial trading tool space.
*   Introduce a premium subscription tier for advanced features (e.g., more indices, faster polling) within the first year.

**Product Goals:**
*   **Simplicity & Abstraction:** A new user must be able to connect their Bybit account and execute their first synthetic index trade in under five minutes.
*   **Trust & Security:** User API keys must be encrypted with best-in-class security. The platform must operate with 100% transparency about the trades it executes on the user's behalf. Aim for zero critical security incidents.
*   **Reliability:** The trade execution engine must be highly reliable, with robust error handling for API failures or market volatility. System uptime must exceed 99.9%.

## Key Success Measures

*   **Total Value Managed:** The total USDT value of assets in user accounts that are being managed as part of synthetic index positions.
*   **Active Users:** Daily and monthly active users executing trades.
*   **User Retention:** The percentage of users who remain active 30 and 90 days after connecting their account.
*   **Trade Success Rate:** The percentage of initiated index trades that are successfully executed on the user's exchange.

## User Descriptions

**Alex, the Active Analyst:** Alex is an experienced trader who is confident in their analysis of macro trends but finds manual execution on exchanges tedious and inefficient. They want a tool that can execute their strategy flawlessly and manage the underlying assets, allowing them to focus on the big picture. Our platform is the perfect "remote control" for Alex, turning their Bybit account into an index-trading powerhouse.

## Features

**1. User Account & Secure API Key Management:**
*   Standard user onboarding using **NextAuth.js**, which will handle email/password and social provider (e.g., Google) sign-ins.
*   A dedicated and highly secure interface for users to add, validate, and delete their Bybit API keys.
*   Clear instructions on how to create API keys on Bybit with the minimum required permissions (e.g., **Read-Write access for "Contract" -> "Order" and "Position"**). Explicitly state that "Withdrawal" permissions are not needed.

**2. Index Trading Interface:**
*   A clean dashboard that displays the real-time value of supported indices (e.g., BTC.D).
*   A simple trading panel with "Buy" and "Sell" buttons for each index.
*   Users will input the total USDT size of the position they wish to take.
*   The system will check the user's Bybit account balance via the API before allowing a trade.

**3. Position & Performance Dashboard:**
*   A clear view of all open synthetic positions (e.g., "Long BTC.D - $5,000").
*   Real-time calculation and display of the position's Unrealized P&L, based on the current market value of the underlying **futures positions** held in their Bybit account.
*   A "Close Position" button that executes the reverse trades on Bybit to flatten the position.
*   A detailed history of all **futures trades** executed by the platform on the user's behalf.

## What is Not Included (MVP Scope)

*   **Custody of Funds:** The platform will never hold or manage user funds directly.
*   **Automated Strategies:** All trades are initiated manually by the user. There is no "auto-trading" feature.
*   **Support for Other Exchanges:** The MVP will only support Bybit.
*   **Variable Leverage:** All futures trades are executed at **1x leverage only**.
*   **Mobile Application:** The initial launch will be a web-only platform.

## Technical Information

*   **General Technology:** The user interface will be built with **Next.js**. The backend services will be built with **Python**.
*   **Data Source:** Market capitalization data will be sourced from the **CoinGecko** service.
*   **Exchange Integration:** All trade execution will be performed via the official **Bybit API** for **Perpetual Futures Contracts**.
*   **Infrastructure:** The entire system will be deployed on **Render.com**.

## System Quality Requirements

*   **Security:** Encryption of user API keys is the highest security priority. The system must be protected against CSRF, XSS, and other web application vulnerabilities.
*   **Reliability:** The connection to the Bybit API must be resilient. The system must gracefully handle API rate limits, downtime, or errors from the exchange.
*   **Data Integrity:** The platform's internal tracking of synthetic positions must be regularly reconciled with the actual **open futures positions** in the user's Bybit account.
*   **Maintainability:** The backend will be built with a modular architecture to isolate user management, trade execution logic, and position tracking.
