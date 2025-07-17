FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3005

# Development command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3005"]