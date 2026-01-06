# Technical Assignments

This repository contains technical assignments for software engineer recruitment.

## Frontend Exercise: Industrial Automation Dashboard

### Overview

This exercise focuses on building a frontend application for an industrial automation user interface. You will be working with a simulated backend REST API that provides real-time data from industrial equipment, and your task is to create a professional dashboard that allows a client operator to monitor and interact with the system.

### Objective

Design and implement a modern, user-friendly dashboard that displays industrial automation data in a clear and actionable manner. The dashboard should provide operators with the information they need to monitor system status, identify issues, and make informed decisions.

### Requirements

1. **Set up a frontend project** using a framework/library of your choice (React, Vue, Angular, Svelte or others)
2. **Connect to the provided REST API** to fetch and display data from all available endpoints
3. **Design a dashboard interface** that includes:
   - Site selection functionality (users can select a site and view its assets)
   - Real-time data visualization (charts, graphs, time series)
   - Storage level alerts
4. **Implement asset management features**:
   - Display asset information (name, type, capacity, efficiency, cost)
   - Support updating asset data via the PATCH endpoint (name, capacity, efficiency, cost_per_mwh)
   - Show updated asset information in the dashboard
5. **Implement best practices** for code organization, error handling, and user experience

### Getting Started

1. Clone this repository
2. Review the API documentation (see `api/` directory for details)
3. Set up your frontend project in a new directory
4. Start the simulated backend API (instructions provided in `api/README.md`)
5. Build your dashboard application

### Evaluation Criteria

Your solution will be evaluated based on:
- **Code quality**: Clean, maintainable, and well-organized code
- **User experience**: Intuitive interface design and smooth interactions
- **Functionality**: Correct implementation of features and API integration
- **Best practices**: Proper error handling, loading states, and responsive design
- **Documentation**: Clear README explaining your setup and design decisions

### Submission

Please submit your solution as a pull request or provide access to your repository. Include:
- Your frontend project code
- A README with setup instructions
- Brief explanation of your design choices and any assumptions made

### Questions?

If you have any questions about the requirements or need clarification, please don't hesitate to ask.

Good luck!
