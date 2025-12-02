FROM alpine:3.19

# Install Core Utilities & Desktop Environment
RUN apk add --no-cache \
    bash \
    curl \
    git \
    python3 \
    py3-pip \
    nodejs \
    npm \
    xfce4 \
    xfce4-terminal \
    faenza-icon-theme \
    xvfb \
    x11vnc \
    supervisor \
    sudo \
    ttf-dejavu \
    chromium

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone https://github.com/novnc/websockify /opt/novnc/utils/websockify \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# Create ZKputer User
RUN addgroup -S zkputer && adduser -S zkputer -G zkputer \
    && echo "zkputer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && echo "zkputer:zkputer" | chpasswd

# Setup Workspace
WORKDIR /home/zkputer
USER zkputer

# Configure XFCE to look "Cyberpunk" (Dark Mode defaults)
RUN mkdir -p /home/zkputer/.config/xfce4/terminal \
    && mkdir -p /home/zkputer/.vnc

# Copy Configuration Files
COPY --chown=zkputer:zkputer config/terminalrc /home/zkputer/.config/xfce4/terminal/terminalrc
COPY --chown=zkputer:zkputer config/supervisord.conf /etc/supervisord.conf

# Copy ZKputer Source Code
COPY --chown=zkputer:zkputer ../src /home/zkputer/zkputer
COPY --chown=zkputer:zkputer ../demo.py /home/zkputer/demo.py

# Install Python Dependencies
RUN pip3 install --user --break-system-packages requests aiohttp

# Expose Ports (VNC & noVNC)
EXPOSE 5900 6080

# Start Supervisor
CMD ["sudo", "/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
