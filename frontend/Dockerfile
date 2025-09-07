FROM node:22.12-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=development

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Create non-root user - for security
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]