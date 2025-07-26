import reflex as rx
from ..states.file_storage_state import FileStorageState
from .modern_progress_bar import file_upload_progress_card


def creative_upload_animation() -> rx.Component:
    """Create a creative upload animation with particle effects."""
    return rx.vstack(
        rx.html("""
    <div class="upload-animation-container">
        <div class="upload-icon-wrapper">
            <svg class="upload-icon" width="80" height="80" viewBox="0 0 24 24" fill="none">
                <path class="arrow-path" d="M12 15V3m0 0l-4 4m4-4l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17l.621 2.485A2 2 0 004.561 21h14.878a2 2 0 001.94-1.515L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="particle-container">
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
            </div>
        </div>
        <div class="upload-text">Uploading files...</div>
        <div class="progress-ring">
            <svg width="120" height="120">
                <circle class="progress-ring-circle" cx="60" cy="60" r="50" />
                <circle class="progress-ring-fill" cx="60" cy="60" r="50" />
            </svg>
        </div>
        
        <style>
        .upload-animation-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        
        .upload-icon-wrapper {
            position: relative;
            margin-bottom: 1rem;
        }
        
        .upload-icon {
            color: #3b82f6;
            animation: float 2s ease-in-out infinite;
        }
        
        .arrow-path {
            animation: arrow-move 1.5s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes arrow-move {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .particle-container {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            pointer-events: none;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(45deg, #3b82f6, #60a5fa);
            border-radius: 50%;
            opacity: 0;
        }
        
        .particle:nth-child(1) {
            top: 50%;
            left: 50%;
            animation: particle-1 2s ease-out infinite;
        }
        
        .particle:nth-child(2) {
            top: 50%;
            left: 50%;
            animation: particle-2 2s ease-out infinite 0.25s;
        }
        
        .particle:nth-child(3) {
            top: 50%;
            left: 50%;
            animation: particle-3 2s ease-out infinite 0.5s;
        }
        
        .particle:nth-child(4) {
            top: 50%;
            left: 50%;
            animation: particle-4 2s ease-out infinite 0.75s;
        }
        
        .particle:nth-child(5) {
            top: 50%;
            left: 50%;
            animation: particle-5 2s ease-out infinite 1s;
        }
        
        .particle:nth-child(6) {
            top: 50%;
            left: 50%;
            animation: particle-6 2s ease-out infinite 1.25s;
        }
        
        .particle:nth-child(7) {
            top: 50%;
            left: 50%;
            animation: particle-7 2s ease-out infinite 1.5s;
        }
        
        .particle:nth-child(8) {
            top: 50%;
            left: 50%;
            animation: particle-8 2s ease-out infinite 1.75s;
        }
        
        @keyframes particle-1 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(-40px, -40px) scale(0); opacity: 0; }
        }
        
        @keyframes particle-2 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(40px, -40px) scale(0); opacity: 0; }
        }
        
        @keyframes particle-3 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(-40px, 40px) scale(0); opacity: 0; }
        }
        
        @keyframes particle-4 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(40px, 40px) scale(0); opacity: 0; }
        }
        
        @keyframes particle-5 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(-60px, 0) scale(0); opacity: 0; }
        }
        
        @keyframes particle-6 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(60px, 0) scale(0); opacity: 0; }
        }
        
        @keyframes particle-7 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(0, -60px) scale(0); opacity: 0; }
        }
        
        @keyframes particle-8 {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(0, 60px) scale(0); opacity: 0; }
        }
        
        .upload-text {
            font-size: 1.2rem;
            color: #e5e7eb;
            margin-bottom: 1.5rem;
            font-weight: 500;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.8; }
            50% { opacity: 1; }
        }
        
        .progress-ring {
            position: relative;
            transform: rotate(-90deg);
        }
        
        .progress-ring-circle {
            fill: none;
            stroke: rgba(59, 130, 246, 0.1);
            stroke-width: 4;
        }
        
        .progress-ring-fill {
            fill: none;
            stroke: #3b82f6;
            stroke-width: 4;
            stroke-dasharray: 314;
            stroke-dashoffset: 314;
            animation: progress 2s ease-out infinite;
            filter: drop-shadow(0 0 6px rgba(59, 130, 246, 0.5));
        }
        
        @keyframes progress {
            0% { stroke-dashoffset: 314; }
            50% { stroke-dashoffset: 157; }
            100% { stroke-dashoffset: 0; }
        }
        </style>
    </div>
    """),
        file_upload_progress_card(),
        spacing="4",
        width="100%",
        align="center",
    )


def file_appear_animation() -> rx.Component:
    """Animation styles for files appearing in the list."""
    return rx.html("""
    <style>
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .file-list-item {
        animation: slideIn 0.3s ease-out forwards;
    }
    
    .file-list-item:nth-child(1) { animation-delay: 0.05s; }
    .file-list-item:nth-child(2) { animation-delay: 0.1s; }
    .file-list-item:nth-child(3) { animation-delay: 0.15s; }
    .file-list-item:nth-child(4) { animation-delay: 0.2s; }
    .file-list-item:nth-child(5) { animation-delay: 0.25s; }
    
    @keyframes sparkle {
        0% { transform: scale(0) rotate(0deg); opacity: 0; }
        50% { transform: scale(1) rotate(180deg); opacity: 1; }
        100% { transform: scale(0) rotate(360deg); opacity: 0; }
    }
    
    .upload-success-sparkle {
        position: absolute;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, #3b82f6 0%, transparent 70%);
        animation: sparkle 1s ease-out;
    }
    </style>
    """)