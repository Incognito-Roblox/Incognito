content=r"""

<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
    <meta charset="UTF-8">
    <title>Incognito BETA</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
        }

        body {
            display: flex;
            flex-direction: row;
            background-color: #242424;
            color: #e2e2e2;
            font-family: "Inter", sans-serif;
            font-style: normal;
            font-weight: 300;
            overflow: hidden;
        }

        body * {
            transition: width 0.14s ease, height 0.3s ease;
        }

        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
            margin-top: 4px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
            margin-top: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #303030;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #3b3b3b;
        }


        .left-container {
            position: relative;
            background-color: #282828;
            width: 300px;
            height: 98%;
            margin-top: 32px;
            border-right: 1px solid #454545;
            transition: none;
        }

        .top-left-container {
            margin-top: -10px;
            padding: 3px 20px
        }

        .info-container {
            display: flex;
            align-items: center;
        }

        .info-container > img {
            margin-top: 7px;
            margin-right: 14px;
            width: 35px;
            height: 35px;
        }

        .info-text > h2 {
            font-size: 16px;
            margin-bottom: 0;
            margin-top: 12px;
        }

        .info-text > span {
            color: #a8a8a8;
            font-size: 12px;
        }
        .spacer {
            flex-grow: 1;
        }

        .filesystem-buttons {
            display: flex;
            background-color: #303030;
            border-radius: 7px;
            margin-top: 15px;
            padding: 9px 13px;
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
        }

        .filesystem-buttons > img {
            width: 18px;
            height: 18px;
            margin-right: 10px;
            cursor: pointer;
        }

        .undo-buttons {
            display: flex;
            margin-left: 50px;
            gap: 20px;
        }

        .undo-buttons > img {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }

        .bottom-left-container {
            margin-top: 10px;
            font-weight: 500;
        }

        .folder-header {
            display: flex;
            position: relative;
            align-items: center;
            padding: 10px 29px;
            font-size: 13px;
            gap: 10px;

        }

        .folder-header > img {
            width: 15px;
            height: 15px;
        }

        .folder-arrow {
            position: absolute;
            right: 30px;
        }
        .collapse-icon, .expland-icon {
            margin-left: auto;
            cursor: pointer;
        }

        .files-container-wrapper {
            position: relative;
            max-height: 250px;
            overflow: hidden;
            overflow-y: scroll;
            padding-bottom: 5px;
            transition: max-height 0.3s ease-in-out;
        }

        .files-container {
            margin-top: 5px;
            overflow-y: scroll;
            overflow-x: hidden;
        }

        .file-wrapper {
            padding-left: 40px;
            width: 100%;
        }

        .file-wrapper:hover {
            background-color: #303030;
        }

        .file {
            display: flex;
            align-items: center;
            width: 100%;
            padding: 9px 4px;
            font-size: 12px;
            cursor: pointer;
        }

        .file > img {
            width: 15px;
            height: 15px;
            margin-right: 7px;
        }

        .main-container {
            padding: 13px;
            flex-grow: 1;
            overflow: hidden;
            margin-top: 25px;
        }

        .actions {
            display: flex;
            justify-content: space-between;
            align-items: center; 
            width: 100%
        }

        .action-buttons {
            display: flex;
            justify-content: space-between;
            gap: 4px;
        }

        .action-buttons > div {
            display: flex;
            align-items: center;
            background-color: #303030;
            border-radius: 6px;
            padding: 10px;
            width: 20px;
            height: 20px;
            cursor: pointer;
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
            overflow: hidden;
            white-space: nowrap;
            transition: width 0.2s ease-in-out;
        }

        .action-buttons > div > span {
            visibility: hidden;
            opacity: 0;
            transition: visibility 0s, opacity 0.5s ease;
            padding-left: 6px;
            font-weight: 600;
        }

        .action-buttons > div:hover > span {
            visibility: visible;
            opacity: 1;
        }

        .action-buttons > div > img {
            width: 20px;
            height: 20px;
        }

        .action-buttons > div:hover {
            background-color: #363636;
            width: 93px;
        }

        .tabs-wrapper, .tabs-gradient-wrapper {
            display: flex;
            align-items: center;
            position: relative;
            justify-content: space-between;
            width: 100%;
            max-width: 100%;
            height: auto;
            overflow: hidden;
        }

        .tabs-gradient-wrapper::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to right, #242424 -20px, rgba(0, 0, 0, 0) 40px, rgba(0, 0, 0, 0) calc(100% - 80px), #242424);
            pointer-events: none;
        }
        .tabs-container {
            display: flex;
            width: calc(100% - 10px); 
            align-items: center;
            gap: 6px;
            margin-top: 8px;
            overflow-y: hidden;
            overflow-x: scroll;
            position: relative;
        }

        .tab {
            display: flex;
            align-items: center;
            background-color: #303030;
            padding: 10px;
            border-radius: 7px;
            gap: 4px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            justify-content: space-between;
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
            animation: fadeInSlideUp 0.2s ease;
        }

        .tab > img {
            width: 16px;
            height: 16px;
        }

        .tab > img:nth-of-type(2) {
            margin-left: auto;
            width: 12px;
            height: 12px;
            cursor: pointer;
        }

        .tab:hover {
            background-color: #363636;
        }
        .tab.active {
            border: 1px solid #ffffff;
            background-color: #3b3b3b;
        }

        .editor-container {
            overflow: hidden;
            border-radius: 10px;
            border: 1px solid rgb(65, 63, 63);
            margin-top: 10px;
            height: 100%;
            max-height: calc(100% - 106px);
            width: 100%;
        }

        #newTab {
            padding: 12px;
            background-color: #303030;
            border-radius: 7px;
            cursor: pointer;
            width: 17px;
            height: 17px;
            margin-top: 5px;
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
        }

        #newTab:hover {
            background-color: #363636;
        }

        .drag {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: absolute;
            background-color: #303030;
            width: 100%;
            height: 30px;
            border-bottom: 1px solid #454545;
        }

        .drag-icon {
            width: 12px;
            height: 12px;
            margin-left: 10px;
        }

        .left-drag-bar {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 8px;
        }

        .left-drag-bar > span {
            font-size: 9px;
        }
        .top-island {
            display: flex;
            align-items: center;
            gap: 7px;
            justify-content: center;
            flex-grow: 1;
        }
        .icon-container {
            align-items: center;
            border-radius: 6px;
            padding: 5px;
            width: 15px;
            height: 15px;
            cursor: pointer;
            overflow: hidden;
            white-space: nowrap;
            position: relative;
            transition: all 0.3s ease;
        }

        .icon-container  > img {
            width: 15px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.3s ease;
        }

        .icon-container:hover img {
            width: 22px;
            transform-origin: center;
        }

        .underline {
            position: absolute;
            bottom: 0;
            height: 2px;
            background-color: white;
            width: 16px;
            transition: left 0.3s ease, width 0.3s ease;
        }

        .buttons {
            display: flex;
            align-items: center;
            gap: 1px;
            width: 80px;
            height: 100%;
        }
        
        #close > img, #minimize > img {
            width: 12px;
            height: 12px;
            margin: 0 5px;
            background-color: transparent;
            color: white;
            border: none;
            cursor: pointer;
        }

        #close, #minimize {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            width: 80px;
        }

        #close:hover, #minimize:hover {
            background-color: #3a3a3a;
            color: white;
        }

        #attach > img {
            width: 20px;
            height: 20px;
        }

        .status-holder {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 4px;
        }

        .action-buttons > div {
            cursor: pointer;
        }   

        .status-holder > div:first-child, .action-buttons > div {
            background-color: #303030;
            border-radius: 6px;
            padding: 10px;
            width: 20px;
            height: 20px;
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
        }

        .status-holder > div:first-child:hover, .action-buttons > div:hover {
            background-color: #363636;
        }

        .status-holder > div:first-child {
            border-top-right-radius: 0;
            border-bottom-right-radius: 0;
            cursor: pointer;
        }

        .status {
            position: relative;
            width: 10px;
            height: 10px;
            margin-top: 2px;
            background-color: red;
            border: 1px solid white;
            border-radius: 50%;
        }

        .holder {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
            padding: 12px;
            background-color: #303030;
            border-radius: 7px;
            height: 16px;
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
        }

        .file-name-input {
            outline: none;
            border: 1px solid #585858;
            color: white;
            border: 4px;
            background-color: #414141;;
        }

        .notification {
            position: fixed;
            z-index: 9999999999999;
            bottom: -100px;
            left: 50%;
            transform: translateX(-50%) scale(0);
            background-color: #303030;
            color: #e2e2e2;
            padding: 20px 30px;
            border-radius: 50%;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            box-shadow: inset 0 1px 2px 0 rgba(255, 255, 255, 0.08);
            transition: all 0.2s ease;
            width: 0;
            height: 0;
            overflow: hidden;
            text-align: center;
        }

        .notification-title {
            color: #ffffff;
            font-size: 14px;
            margin-bottom: 5px;
            font-weight: bold;
            opacity: 0;
            transform: translateY(-10px);
            transition: opacity 0.3s ease, transform 0.3s ease;
            transition-delay: 0.8s;
        }

        .notification-message {
            color: #d9d9d9;
            font-size: 12px;
            opacity: 0;
            transform: translateY(-10px);
            transition: opacity 0.3s ease, transform 0.3s ease;
            transition-delay: 0.95s;
        }

        .notification.show .notification-title, .notification.show .notification-message {
            opacity: 1;
            transform: translateY(0);
        }

        .notification.show {
            animation: showNotification 0.8s forwards;
        }

        .notification.hide .notification-title,
        .notification.hide .notification-message {
            opacity: 0;
            transform: translateY(-10px);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        .loading {
            background: orange;
            animation: pulse 1.5s infinite ease-in-out;
        }

        .files-container-wrapper.collapsed {
            max-height: 0;
        }

        .collapse-icon {
            transition: transform 0.3s ease-in-out;
        }

        .rotated {
            transform: rotate(180deg);
        }

        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 0 0 0 rgba(255, 165, 0, 0.4);
            }
            50% {
                box-shadow: 0 0 0 10px rgba(255, 165, 0, 0);
            }
        }

        @keyframes showNotification {
            0% {
                bottom: 10px;
                width: 0;
                height: 0;
                border-radius: 50%;
                transform: translateX(-50%) scale(0);
            }
            50% {
                bottom: 20px;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                transform: translateX(-50%) scale(1);
            }
            100% {
                bottom: 30px;
                width: 300px;
                height: auto;
                border-radius: 9px;
                transform: translateX(-50%) scale(1);
            }
        }
        @keyframes hideNotification {
            0% {
                bottom: 30px;
                width: 300px;
                height: auto;
                border-radius: 9px;
                transform: translateX(-50%) scale(1);
            }
            50% {
                bottom: 20px;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                transform: translateX(-50%) scale(1);
            }
            100% {
                bottom: -100px;
                width: 0;
                height: 0;
                border-radius: 50%;
                transform: translateX(-50%) scale(0);
            }
        }
        @keyframes slideFadeIn {
            from {
                transform: translate(-50%, -50%) translateY(20px) translateZ(0);
            }
            to {
                transform: translate(-50%, -50%) translateY(0) translateZ(0);
            }
        }

        @keyframes slideFadeOut {
            from {
                transform: translate(-50%, -50%) translateY(0) translateZ(0);
            }
            to {
                transform: translate(-50%, -50%) translateY(20px) translateZ(0);
            }
        }

        @keyframes lightScan {
            0%, 100% { background-position: -100% 0; }
            50% { background-position: 100% 0; }
        }


        @keyframes fadeInSlideUp {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .loadingFade {
            border-radius: 8px;
            background: linear-gradient(to right, #242424 10%, #2d2d2d 50%, #242424 90%);
            background-size: 200% 100%;
            animation: lightScan 2s infinite;
            color: transparent;
        }

        .loadingFade > :not(img) {
            visibility: hidden;
        }

        .main-background {
            display: flex;
            flex-grow: 1;
            overflow: hidden;
        }

        .settings-background {
            display: none;
            margin-top: 30px;
            width: 100%;
            height: 100%;
            background-color: #242424;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale; 
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        
        .settings-container {
            display: flex;
            height: 100%;
            width: 100%;
        }

        .settings-left {
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex: 0 0 200px;
            padding: 17px;
            
        }

        .settings-category {
            display: flex;
            align-items: center;
            gap: 8px;
            background-color: #2c2c2c;
            border-radius: 7px;
            padding: 10px 10px;
            width: 200px;
            border: 1px solid #413f3f;
            cursor: pointer;
            color: #c0c0c0;
        }

        .settings-category:hover {
            background-color: #333333;
            border: 1px solid #525252;
            color: #cecece;
        }

        .settings-category > span {
            font-size: 14px;
        }

        .settings-category > img {
            width: 17px;
            height: 17px;
        }

        .settings-category.active {
            border: 1px solid #616161;
            background-color: #3a3a3a;
            color: #ffffff;
        }

        #settings-close {
            cursor: pointer;
        }

        .settings-main-wrapper {
            position: relative;
            height: 100%;
            width: 100%;
            max-height: calc(100% - 96px);
            margin-top: 17px;
            margin-right: 17px;
            border-radius: 7px;
            overflow: hidden;
            border: 1px solid #413f3f;
            padding-bottom: 20px;
        }

        .settings-main {
            display: flex;
            flex-direction: column;
            gap: 14px;
            flex: 1;
            background-color: #2c2c2c;
            padding: 17px;
            height: 100%;
            overflow: hidden;
            overflow-y: scroll;
        }

        .gradient-overlay {
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 100%;
            background: linear-gradient(to bottom, #2c2c2c -1%, transparent 5%, transparent 95%, #2c2c2c 100%);
            pointer-events: none;
        }

        .settings-main::-webkit-scrollbar-thumb {
            background-color: #424242;
        }

        .setting-header {
            display: flex;
            gap: 6px;
            margin-left: -2px;
            background-color: #424242;
            border: 1px solid #6d6d6d;
            border-radius: 5px;
            width: 100%;
            max-width: calc(100% - 20px);
            height: 20px;
            padding: 5px 10px;
            align-items: center;
        }

        .setting-header > img {
            width: 14px;
            height: 14px;
        }
        
        .setting-header > span {
            font-size: 13px;
        }


        .setting-option {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .setting-option-info {
            display: flex;
            flex-direction: column;
        }

        .settings-title {
            display: block;
            font-size: 13px;
            font-weight: 400;
            color: #cecece;
        }

        .settings-description {
            display: block;
            font-size: 9px;
            font-weight: 500;
            color: #8b8888;
            margin-top: 3px;
        }

        .settings-option-button-1 {
            display: flex;
            align-items: center;
            height: 25px;
            border-radius: 4px;
            padding: 12px;
            color: #d8d8d8;
            font-weight: 500;
            font-size: 11px;
            background-color: #424242;
            border: 1px solid #6d6d6d;
            cursor: pointer;
        }

        .settings-option-button-2 {
            width: 25px;
            height: 25px;
            border-radius: 4px;
            background-color: #424242;
            border: 1px solid #6d6d6d;
            cursor: pointer;
        }

        .settings-option-slider {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .settings-option-button-3 {
            -webkit-appearance: none;
            width: 60px;
            height: 5px;
            background: #424242;
            outline: none;
            opacity: 0.7;
            -webkit-transition: .2s;
            transition: opacity .2s;
            cursor: pointer;
            border-radius: 4px;
        }

        .settings-option-button-3::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #6d6d6d;
            cursor: pointer;
        }

        .slider-value {
            color: #d8d8d8;
            font-weight: 500;
            font-size: 11px;
        }

        .settings-option-button-1:hover, .settings-option-button-2:hover {
            background-color: #4e4e4e;
            border: 1px solid #7a7a7a;
        }

        .settings-option-button-3::-webkit-slider-thumb:hover {
            background-color: #8a8a8a;
        }
    

        .left-container-handle {
            position: absolute;
            width: 6px;
            height: 100%;
            z-index: 99999;
            right: 0;
            cursor: e-resize
        }

        .handle {
            position: absolute;
            width: 6px;
            height: 6px;
            z-index: 99999;
        }
        #top-left-handle { top: 0; left: 0; cursor: nw-resize; z-index: 999999; }
        #top-right-handle { top: 0; right: 0; cursor: ne-resize; z-index: 999999; }
        #bottom-left-handle { bottom: 0; left: 0; cursor: sw-resize; z-index: 999999; }
        #bottom-right-handle { bottom: 0; right: 0; cursor: se-resize; z-index: 999999; }
        #left-handle { height: 100%; top: 50%; left: 0; transform: translateY(-50%); cursor: w-resize; }
        #right-handle { height: 100%; top: 50%; right: 0; transform: translateY(-50%); cursor: e-resize; }
        #top-handle { width: 100%; top: 0; left: 50%; transform: translateX(-50%); cursor: n-resize; }
        #bottom-handle { width: 100%; bottom: 0; left: 50%; transform: translateX(-50%); cursor: s-resize; }
        
        .seperator {
            background-color: rgb(138, 138, 138);
            width: 5px;
            height: 5px;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <div id="top-left-handle" class="handle"></div>
    <div id="top-right-handle" class="handle"></div>
    <div id="bottom-left-handle" class="handle"></div>
    <div id="bottom-right-handle" class="handle"></div>
    <div id="left-handle" class="handle"></div>
    <div id="right-handle" class="handle"></div>
    <div id="top-handle" class="handle"></div>
    <div id="bottom-handle" class="handle"></div>
    <div class="drag">
        <div class="left-drag-bar">
            <img draggable="false" src="data:image/png;base64,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" class="drag-icon">
            <h2>INCOGNITO</h2>
            <div class="seperator"></div>
            <span> v1.1.6dev</span>
        </div>
        <div class="top-island">
            <div class="loadingFade icon-container"><img draggable="false" id="editor" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEQUlEQVR4nO2cTahVVRTHr0FKGpETDZvYpN5r4iCnfUBNNGqik1AqqEYZlHMNqlGG5sA0sEIhDQILaqQO8jWLoJFFk6Ampmj5WRHv7y/uuZfHq87e55zr/jr3rR9ceIN39lp7vf32f6+19rmDgWEYhmEYhmEYhmEYRnuAZR1+3egKsALpPaSrSH8iHQbu6DyQ4QdpHzdv8q+PdLDhMaMLwG1Iv9cE+kqngQw/wMz/gjwK9OWGR40uANsdgZ7rNJAxwf48CvTehkeNLiB9XRto2NZpIKNRCK86Aj3jedToAjDr2DauDf8InQYz3JgQJgITwmSBPuPYn7dPfc0EWI90Emke6RywI4MQzk445iqkD5D+GH8ODOsog9IYO/p9zcS3JMwIJxZCpPdrxjs8KA2kQ47JnwhuC7aFzgiRrjv+Q4IvlIkBnq51cjT5T4Pbk/Y6bO2b0P9lw0KUY8yLwL2h5zCJk/cgXXAGGp7sgxAi7fcsllNZz+bjlfCFx8EjfckIGWnMj54F81rYmXRzbocnyD8Bd/UpIwQeQvrbMf5fwIZwM2nv1Gx1DKp3SsCjiUujZwKNv8uzeM4mbZON+3TfeRx6o68ZIaOt6SvP3N4NYaedM9IejyPfArf3uTQK3Oc5hQyNbQ5ly+fEI1XmV+/EdeD+aSiNAs96FtN5YG1Ie/81fjfSzx5lfmGaSqNIxz3B/jy0vbaGP4tmOJEQTrCwXoxh9DlPkH8F1gQ3WkBpFHi4Yat8YDBV4jDI1yNEeju6+Lc47kxUX+hTj3AYSKRvPDF4M4SR3SUc4MncIxwnaDeiJGjAxlJSUhILocOHlz2L7hdgdYwiy6tRZlNwj7BFEe1ouImNBjyZurdGpB5hZz9gbZWwuBdgt4NBVfB2F8LXRZtJoh7hrQA8VZ226uNzrM+BnskphLEDXczWQYQeYcStY1NvxZAChDCaGJZ0vEOaK+HWaJTj3cLg8/Ov50xYKOTWaIuE5bEQE60/WiVIwSng1miLFPyt3heVKCEjbC4qLQ9nDJ7PUSYlsxAmLZMuGJU+SV34J6MQtij8vzQVrSwyC2G2Vtai5qxSNGfJKIRZm7MLTkjvpLhuQCYhbCH+we8TZr1AQ54eYVNHaX8s2y6HHox9JYwMQljUlbBFTr0S65IjGYSwyEuOi4osX8a4tkvqyzLNRbSdoW2Gvoj+RB9Ko8PLi54Fc7qIl0QbXq04UsLrEy3sXXLYu1TEqxUtXhY62oceobOjBFsHJTHe487WnD4e70OP0PGVQeW9/rZovz5R/btJPwDP9KVHCCyvgi39Vq3u4c8hq3IlQgGl0SUBhfQIpx4K6RFONfiFMHyRfalCAT3CJQEmhIkCLRPCVIGeMyFME+jLKTPCJQt1X1AyDL4JYfBAf1gT6AOBzRjAnUgfV52O0ecjYKVFJmYDmCkv6hiGYRiGYRiGYRiGMQjMP/4Yv/FE4HhAAAAAAElFTkSuQmCC"></div>
            <div class="loadingFade icon-container"><img draggable="false" id="settings" src="data:image/png;base64,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"></div>
            <div class="underline loadingFade"></div>
        </div>
        <div class="buttons">
            <div id="minimize"><img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA00lEQVR4nO3XS0pDMRiA0c4EFV2Exe35GErdoDoTRamL0AXIJ4U7sNDObl/0nA0k/0cIyWQCAAAAAAAAAAAAAAAAAIetOqvuq5fqp+PzPcx+t2ixqcjX1fuuJ90jb9V07MjnIq/0WV2OGfpx9TpUszFDf0m61nysyCfV7/p1jt7vopHQhxJ6ONXzLWz4uK+OIfRs19PssYexn3eLdyPLPqqL0UIPsadiL3mtrkaN/C/2aXVbPQ/f0WPzXT1VN4sWG4kMAAAAAAAAAAAAAAAAAJOt+QNLPz1PJ96JVgAAAABJRU5ErkJggg=="></div>
            <div id="close"><img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB40lEQVR4nO2cS2rDQBBEtYpz8ijnyWLQhfK5RRmBDAaHENszPVXd9UDglal+SK0RGvWyGGOMMcYYY4wxxpgbAJwAvAP4Po7990lFFRTyA3gB8IFbNgCvCzkS+f8IyRdWNf8/QvKEVc1/R0hK2RL5HwhJJVsi/3F3bnicNvNuLpP/WPY8S5shu4PkC2tE2H2N2YMtso080S5+40dJdJjszpJ3PpeA0Cv60ka2kY7t4pq3UXlHB28jZCtljboUu7cRhYzyhYA4W5qCQJipC0yFgSjLEBgKBEGGEGYWiiqSZxaMapJnFI6qkiMFoLrkCBGw5LBH4DbgP7neeN/LoLOvdrsQlL2lkUwse0snmVB2XslEsvNLJpBdR/JE2fUkT5BdV3KgbEsOkG3J11h0AHDrSCH5Qt0WAi/vUkqud2bDj+AlJOc/s8EjOa9s8EnOJ5tYch7ZfjkbgLcbBOANNAF4S1gA3uQYgLftBsCwFw4EGYbCVCCIsnSFsTAQZnoK5oJAnC1dIRDImOazXwhlHTWvQ/2je6l5HcpjJKTmdWzCg1Fk5nU08VE/EvM6modXZRpnliW/xIC+LPklRk5myS8xRDVLfomxwFnyH6uRfen3dRyr0me/EM9vjDHGGGOMMcYYswRyBpias+umnbidAAAAAElFTkSuQmCC"></img></div>
        </div>
    </div>
    <div class="settings-background">
        <div class="settings-container">
            <div class="settings-left">
                <div class="settings-category active">
                    <img src="data:image/png;base64,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">
                    <span>General</span>
                </div>
                <div class="settings-category">
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEK0lEQVR4nO2dTagWVRyHj6blB1KIQRQhFIKllZJBVGCY25ZtWgi2kNAi3dSigloUgle0ZbVr2aoI20SpdS2KRCQUtbQvv41CorCP33ninHfog7nvbWbufM//gRfuvdyZM+dhZt4553f+7+ucYRiGYRiGYRiGURxgAfA40iTST8lrMv4NFsxg10YAuBrYhHQW75nyJV0EngHmx42M7ABzgQ1Ip8YKTgv/HngKuCZHU8MEmA08gvRlZsFp4d/GqwDmNN2fNgs+XlhwWvjXifCr3NABZgEPIx0qTXBa+NF4G4LZbogA65E+r0xwWvgX8aqBWW4IAA8g7a9NcFr4p+Eqcn0FuB/pg8YEp4V/DDzk+gJwL9I7jYsdLzwMfNa6rgLcgfQmkm9cZjbh7wFrXFcAVnRKsJ9S+GrXVoDlSG8g/dm4LD9j2T7e7uBO1xaApUivIv3RuCBfunDFqxOWNSn4ZqRXkK40LsRXLvz3eLXCLXUKnos0MQjBPiX8CtKO4KB60dLOxjvsGxe+ow7RPzTeUd+46Esm2tci+mIdoicaP6P8EG4dozfD8LShAQoW0u5a3gz/Jfz2ZIDSf+H6ewDT3IgRWNnpIbfPNCS/27WFMFyNwvsl+B7XVlo/LeozTZs+6Do20f9+hwQf6HQQkERX+1os+JNeRVuMwtjPWiT4cK/DWkbCDzYoeDhpOHWs5+jr+o6YsMDzwE05Vyg9WuoKpbTg47GNHIJDH5K+LHetTVik3+LvcGOBJWEnShT8Td41eMD1SNuRfu1OwjKaJA/CbyiwivSrGQj+Lu+qUmBJIviX/0lYbnV1kUwq7YxnbraO/4z0ErA457roLUincwg+DWwO2+ZoZzHSy/EYs7URrtaJdics0mWkF4BrM7cF84CtSOen2e+55Ayel2O/1yG9GI+ptwmL9CPwLLCoQGnFR3H70evDvKUVoU3gubj9YBIW6RLwNLCw8mOGhbH8IrQ52IRFOh9vDxXUoIR9AtuQLnQ1Ydld+oS/dAZ4oowalLAP4Mlpi4yKHWN43NtVd8JyWyUJi/I/nk3xeHiyooRlVTU2s3XuLqS3S09YpFPAxiwDjvA/wGOxbqV8wW+FPrq2EJa8Ir1bakd9UkcovRbnRkJOOXpyWJT8HOZLXi/tTe6/7e5p9TLeniQsa11XAO7rWMIyCaxzHU9Y9rZYsCUs1JCwuL5C3fWFacGWsFCt4COWsKjShOWYJSwJlrBMgyUs/UlYNlvCUuxeedkSljxntCUsWMIyBktYvCUsY7GERZawYAmLL/KUYgnLmFuKJSx1YglLzVjCUjOWsNQMLa1hcX0FS1h6X8NypBcJSxH4p6TiWIWCw/O4fepumxKWwUBDNSxDF74pZ8JyIfms/8wlFkb6yxTOTCPYvkyhLCiphsUwDMMwDMMwDMNwaf4CW/PMvLAZGxoAAAAASUVORK5CYII=">
                    <span>Layout</span>
                </div>
                <div class="settings-category">
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEE0lEQVR4nO2dS4jNURzHj1FKiFgo7/fCFLFhg2FYkoVHaigpVh4rYzc3RUjKozxGFpIoO8VKHllYIYxXk0c2njMY3aL46HAml5k79/7/95zz/52/86mpabrN+f4/ffvPPY//HaUikUgkEolEIpFIJA8ABeAasEAFCDAQWAbsA64A7UAH8BHoBB4Al811LgLqsgipBy8lGOHATOAU0EX1tEiQHIRwYDxwPoFcsZJLuQksVkIA1iVscBCSxTQcqAOOpMgdlORMhfNb8tlgJJvQV7HDdI+Z9wcl2YRusCS64ClvU3CSLbf6kYecI4C3QUq23Op6xzkPBSvZcqsLDvMNAT4FLdliq9sc5lsfvGTLra53lE1PrZMwxkUOk6VOQqsL1q7o72z3EuZocpTj10KUhFY/snJFPXO9Tpij1eHkrvYySW01ydcz2i2P31Lyuy9JulfvsRLmT6aXKTKMc7RMcT+3s0XgVorxmyw3uZsOO1f1e4BJwFazLJp5s4HDKcZudbTg9tnGNfU2YL0ZtC2rZgOrUozbbrnJ3byr9XpcSi/UOO7glAv8Yy1L1jxVwteyCzWOdy6F6L1JJi9VSNZcVL7xJRtoBIqkR++EnwTWlhNfpWTr76jEyKZ2yRXFJ5BMpnumQHPCC62qFcB84Aty0GdDBrg3arfZDRk0uVaOKglQfbNbAmuy5jswVUmBys0uBNhkzRklDco3O8Qma94DI5VE6NnsUJusWaMkw59mh9pkzW4VAlQ4ySS8yaeBfip0kN3kg5mcnbYNcpv8Blit8gB+JBfNQlRXglnfAWC4ygP4k9xoxhsErDC3Ar2R8cw8avEKuKM3CMyZvkEqL+DnnlyUdFjeO0TJUXIuIDY5Ss4FxCZHybkAz++T+8gR/vRZ+u0CmADcBeaovIEsyc9LptX5kS1UMrmSLVxyqey5KlQCkRy27MAkhyk7UMlhyQ5cchiycyJZtuycSZYpO6eSZcmWsnahATYAPxyMn+2kxjwKJ0JyN8DmXMkGJuonkBC4kQpsdCT7k/fbCHADQU3+F2CLw2bPUD4AliBYsgfZ+g/uUOUac6ikN74C24FR5qvZ/My7ZA+yd9rK2Ff4J2UGb67xQaGiTcmOZb91vkvTx3m1Ub28Vjc7M8mOZc9ylTeN6NFSjmkBmyzLXu468OMEt44dWTbZcbOdiz5RZuCv5p5c7R/Dok/JJfm3WpI923XQxRZCFrOQbFG2nqz19xH0eqiSLcnepXwATAE+hCq5RtkvgGHKF8C8hLI/VHrGOwvMQpR+xLgaOp2/rSsTcrL5QO5KXNWvVUIBllbx+Xm3gWlZB9X/SuM48NBsAnSZ748BC1UAmI8M2mZKoaV/M8+yXABW5vq8XiQSiUQikUgkElH/NT8BrnSuaGFw3BkAAAAASUVORK5CYII=">
                    <span>Editor</span>
                </div>
                <div class="settings-category">
                    <img style="margin-top: -2px;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC4UlEQVR4nO3cS6gWZRgH8BGlFCSLEDLJwIWSEC2qjbQpCnRjFAVlrlpEbhLtstKQwEWbiKJFkCsv2OXQSuwC3ciF1VJBAjXDhRYIGiJ54RfDNyuZ73yfnul733m/5wezOQycZ/7nOTPvzDxMVYUQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEMDYsxuv4Gr/1YPsFB7ChN39mPIBT+msGt1c5wyKc0H8fVDnDZmW4inurXOEL5XixyhV+VI4tVa7wk3JsrXJVctCYjxVY2Wx3RdAdB41HcLpln8+TLAVL7Wgcm2W/bRF0B0E3p4zrs+z3aQTdXUfP9p86E0F3F3R9EfwGl1v2i6C7Xt7VP2vZL4IuOegflOO1nIPepxzP5hz0C8rwD+7MOeh6zXlY/70x5PjyCLopZim+19/n0O9gXvZBNwXNwzq817yL+yzzbQ/exuoRx5VX0KUSQU8GdrV09CcT+vXTQ/uFfmfquoqCp4ZcQB9PXVsx8DD+agn5LG5LXV+v4W48gY/w75BufjN1nb2ABc37vyfrt974GN+OOQR0tB4YSn0MOXbnWryMd/EljuOKW/M31lTTyOD2fxWexlv1sgs/N6F06U88WE1huM/hIC74/2/Pd7c9bCoaHh3xdroLF5vnNjtwfzVt8FLTYV243owZf4X3m0HNerWxvJpmeAbXbrE7f8VebMfzeAgLUx9TdnAfzo/ozpM41HTnq0135juCmyODlUSbE83p5I7UNfaewQuFtju0I1iSur5iYFNLyPVAy4rUtRUFH7YEvT91XcUxGJFNP8lZOoOVxI1eSV1XcUTQEXRRREdPJOR78HvLObp+mjZ/AiWUD8twxnAHhk0WhZsLesZoGyPUud92Xxsj6O8i6LkF/ZjxnIug5xb0ujGDvhRBR9D5Ex0dQRdFdHQEXRTR0clnkm90cUIllcngG3rjOJq61t4zmPocZVfqOnsP60d8mOSPpN836tB/dgPW7QmHXr8AAAAASUVORK5CYII=">
                    <span>Appearance</span>
                </div>
            </div>
            <div class="settings-main-wrapper">
                <div class="settings-main">
                    <div class="setting-header">
                        <img src="data:image/png;base64,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">
                        <span>General</span>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Reset Settings</span>
                            <span class="settings-description">Pressing this button will reset all settings back to defaul and close the application.</span>
                        </div>
                        <button class="settings-option-button-1">Reset</button>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Show changelog</span>
                            <span class="settings-description">Clicking this will show you the changelog for the lastest version.</span>
                        </div>
                        <button class="settings-option-button-1">Show</button>
                    </div>
                    <div class="setting-header">
                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEK0lEQVR4nO2dTagWVRyHj6blB1KIQRQhFIKllZJBVGCY25ZtWgi2kNAi3dSigloUgle0ZbVr2aoI20SpdS2KRCQUtbQvv41CorCP33ninHfog7nvbWbufM//gRfuvdyZM+dhZt4553f+7+ucYRiGYRiGYRiGURxgAfA40iTST8lrMv4NFsxg10YAuBrYhHQW75nyJV0EngHmx42M7ABzgQ1Ip8YKTgv/HngKuCZHU8MEmA08gvRlZsFp4d/GqwDmNN2fNgs+XlhwWvjXifCr3NABZgEPIx0qTXBa+NF4G4LZbogA65E+r0xwWvgX8aqBWW4IAA8g7a9NcFr4p+Eqcn0FuB/pg8YEp4V/DDzk+gJwL9I7jYsdLzwMfNa6rgLcgfQmkm9cZjbh7wFrXFcAVnRKsJ9S+GrXVoDlSG8g/dm4LD9j2T7e7uBO1xaApUivIv3RuCBfunDFqxOWNSn4ZqRXkK40LsRXLvz3eLXCLXUKnos0MQjBPiX8CtKO4KB60dLOxjvsGxe+ow7RPzTeUd+46Esm2tci+mIdoicaP6P8EG4dozfD8LShAQoW0u5a3gz/Jfz2ZIDSf+H6ewDT3IgRWNnpIbfPNCS/27WFMFyNwvsl+B7XVlo/LeozTZs+6Do20f9+hwQf6HQQkERX+1os+JNeRVuMwtjPWiT4cK/DWkbCDzYoeDhpOHWs5+jr+o6YsMDzwE05Vyg9WuoKpbTg47GNHIJDH5K+LHetTVik3+LvcGOBJWEnShT8Td41eMD1SNuRfu1OwjKaJA/CbyiwivSrGQj+Lu+qUmBJIviX/0lYbnV1kUwq7YxnbraO/4z0ErA457roLUincwg+DWwO2+ZoZzHSy/EYs7URrtaJdics0mWkF4BrM7cF84CtSOen2e+55Ayel2O/1yG9GI+ptwmL9CPwLLCoQGnFR3H70evDvKUVoU3gubj9YBIW6RLwNLCw8mOGhbH8IrQ52IRFOh9vDxXUoIR9AtuQLnQ1Ydld+oS/dAZ4oowalLAP4Mlpi4yKHWN43NtVd8JyWyUJi/I/nk3xeHiyooRlVTU2s3XuLqS3S09YpFPAxiwDjvA/wGOxbqV8wW+FPrq2EJa8Ir1bakd9UkcovRbnRkJOOXpyWJT8HOZLXi/tTe6/7e5p9TLeniQsa11XAO7rWMIyCaxzHU9Y9rZYsCUs1JCwuL5C3fWFacGWsFCt4COWsKjShOWYJSwJlrBMgyUs/UlYNlvCUuxeedkSljxntCUsWMIyBktYvCUsY7GERZawYAmLL/KUYgnLmFuKJSx1YglLzVjCUjOWsNQMLa1hcX0FS1h6X8NypBcJSxH4p6TiWIWCw/O4fepumxKWwUBDNSxDF74pZ8JyIfms/8wlFkb6yxTOTCPYvkyhLCiphsUwDMMwDMMwDMNwaf4CW/PMvLAZGxoAAAAASUVORK5CYII=">
                        <span>Layout</span>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Top Most</span>
                            <span class="settings-description">Pressing this button will keep the Incognito window on top of all other applications.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Lock Window Size</span>
                            <span class="settings-description">Clicking this will lock the window to its current size.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Reduce Animations</span>
                            <span class="settings-description">Clicking this will disable UI animations.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-header">
                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEE0lEQVR4nO2dS4jNURzHj1FKiFgo7/fCFLFhg2FYkoVHaigpVh4rYzc3RUjKozxGFpIoO8VKHllYIYxXk0c2njMY3aL46HAml5k79/7/95zz/52/86mpabrN+f4/ffvPPY//HaUikUgkEolEIpFIJA8ABeAasEAFCDAQWAbsA64A7UAH8BHoBB4Al811LgLqsgipBy8lGOHATOAU0EX1tEiQHIRwYDxwPoFcsZJLuQksVkIA1iVscBCSxTQcqAOOpMgdlORMhfNb8tlgJJvQV7HDdI+Z9wcl2YRusCS64ClvU3CSLbf6kYecI4C3QUq23Op6xzkPBSvZcqsLDvMNAT4FLdliq9sc5lsfvGTLra53lE1PrZMwxkUOk6VOQqsL1q7o72z3EuZocpTj10KUhFY/snJFPXO9Tpij1eHkrvYySW01ydcz2i2P31Lyuy9JulfvsRLmT6aXKTKMc7RMcT+3s0XgVorxmyw3uZsOO1f1e4BJwFazLJp5s4HDKcZudbTg9tnGNfU2YL0ZtC2rZgOrUozbbrnJ3byr9XpcSi/UOO7glAv8Yy1L1jxVwteyCzWOdy6F6L1JJi9VSNZcVL7xJRtoBIqkR++EnwTWlhNfpWTr76jEyKZ2yRXFJ5BMpnumQHPCC62qFcB84Aty0GdDBrg3arfZDRk0uVaOKglQfbNbAmuy5jswVUmBys0uBNhkzRklDco3O8Qma94DI5VE6NnsUJusWaMkw59mh9pkzW4VAlQ4ySS8yaeBfip0kN3kg5mcnbYNcpv8Blit8gB+JBfNQlRXglnfAWC4ygP4k9xoxhsErDC3Ar2R8cw8avEKuKM3CMyZvkEqL+DnnlyUdFjeO0TJUXIuIDY5Ss4FxCZHybkAz++T+8gR/vRZ+u0CmADcBeaovIEsyc9LptX5kS1UMrmSLVxyqey5KlQCkRy27MAkhyk7UMlhyQ5cchiycyJZtuycSZYpO6eSZcmWsnahATYAPxyMn+2kxjwKJ0JyN8DmXMkGJuonkBC4kQpsdCT7k/fbCHADQU3+F2CLw2bPUD4AliBYsgfZ+g/uUOUac6ikN74C24FR5qvZ/My7ZA+yd9rK2Ff4J2UGb67xQaGiTcmOZb91vkvTx3m1Ub28Vjc7M8mOZc9ylTeN6NFSjmkBmyzLXu468OMEt44dWTbZcbOdiz5RZuCv5p5c7R/Dok/JJfm3WpI923XQxRZCFrOQbFG2nqz19xH0eqiSLcnepXwATAE+hCq5RtkvgGHKF8C8hLI/VHrGOwvMQpR+xLgaOp2/rSsTcrL5QO5KXNWvVUIBllbx+Xm3gWlZB9X/SuM48NBsAnSZ748BC1UAmI8M2mZKoaV/M8+yXABW5vq8XiQSiUQikUgkElH/NT8BrnSuaGFw3BkAAAAASUVORK5CYII=">
                        <span>Editor</span>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Font Size</span>
                            <span class="settings-description">Drag this slider to fine-tune you editor font size.</span>
                        </div>
                        <div class="settings-option-slider">
                            <input type="range" class="settings-option-button-3" min="0" max="100" value="50">
                            <span class="slider-value">12</span>
                        </div>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Lua Language Server</span>
                            <span class="settings-description">Pressing this will enable/disable auto-completion and type hints.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Minimap</span>
                            <span class="settings-description">Pressing this will enable/disable the editor minimap.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Smooth Cursor</span>
                            <span class="settings-description">Pressing this will enable/disable smooth cursor movement in the editor.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Smooth Scroll</span>
                            <span class="settings-description">Pressing this will enable/disable smooth cursor scrolling in the editor.</span>
                        </div>
                        <button class="settings-option-button-2"></button>
                    </div>
                    <div class="setting-header">
                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEE0lEQVR4nO2dS4jNURzHj1FKiFgo7/fCFLFhg2FYkoVHaigpVh4rYzc3RUjKozxGFpIoO8VKHllYIYxXk0c2njMY3aL46HAml5k79/7/95zz/52/86mpabrN+f4/ffvPPY//HaUikUgkEolEIpFIJA8ABeAasEAFCDAQWAbsA64A7UAH8BHoBB4Al811LgLqsgipBy8lGOHATOAU0EX1tEiQHIRwYDxwPoFcsZJLuQksVkIA1iVscBCSxTQcqAOOpMgdlORMhfNb8tlgJJvQV7HDdI+Z9wcl2YRusCS64ClvU3CSLbf6kYecI4C3QUq23Op6xzkPBSvZcqsLDvMNAT4FLdliq9sc5lsfvGTLra53lE1PrZMwxkUOk6VOQqsL1q7o72z3EuZocpTj10KUhFY/snJFPXO9Tpij1eHkrvYySW01ydcz2i2P31Lyuy9JulfvsRLmT6aXKTKMc7RMcT+3s0XgVorxmyw3uZsOO1f1e4BJwFazLJp5s4HDKcZudbTg9tnGNfU2YL0ZtC2rZgOrUozbbrnJ3byr9XpcSi/UOO7glAv8Yy1L1jxVwteyCzWOdy6F6L1JJi9VSNZcVL7xJRtoBIqkR++EnwTWlhNfpWTr76jEyKZ2yRXFJ5BMpnumQHPCC62qFcB84Aty0GdDBrg3arfZDRk0uVaOKglQfbNbAmuy5jswVUmBys0uBNhkzRklDco3O8Qma94DI5VE6NnsUJusWaMkw59mh9pkzW4VAlQ4ySS8yaeBfip0kN3kg5mcnbYNcpv8Blit8gB+JBfNQlRXglnfAWC4ygP4k9xoxhsErDC3Ar2R8cw8avEKuKM3CMyZvkEqL+DnnlyUdFjeO0TJUXIuIDY5Ss4FxCZHybkAz++T+8gR/vRZ+u0CmADcBeaovIEsyc9LptX5kS1UMrmSLVxyqey5KlQCkRy27MAkhyk7UMlhyQ5cchiycyJZtuycSZYpO6eSZcmWsnahATYAPxyMn+2kxjwKJ0JyN8DmXMkGJuonkBC4kQpsdCT7k/fbCHADQU3+F2CLw2bPUD4AliBYsgfZ+g/uUOUac6ikN74C24FR5qvZ/My7ZA+yd9rK2Ff4J2UGb67xQaGiTcmOZb91vkvTx3m1Ub28Vjc7M8mOZc9ylTeN6NFSjmkBmyzLXu468OMEt44dWTbZcbOdiz5RZuCv5p5c7R/Dok/JJfm3WpI923XQxRZCFrOQbFG2nqz19xH0eqiSLcnepXwATAE+hCq5RtkvgGHKF8C8hLI/VHrGOwvMQpR+xLgaOp2/rSsTcrL5QO5KXNWvVUIBllbx+Xm3gWlZB9X/SuM48NBsAnSZ748BC1UAmI8M2mZKoaV/M8+yXABW5vq8XiQSiUQikUgkElH/NT8BrnSuaGFw3BkAAAAASUVORK5CYII=">
                        <span>Appearance</span>
                    </div>
                    <div class="setting-option">
                        <div class="settings-option-info">
                            <span class="settings-title">Coming Soon</span>
                            <span class="settings-description">Settings for Appearance are not yet here! Check back later.</span>
                        </div>
                        
                    </div>
                </div>
                <div class="gradient-overlay"></div>
            </div>
        </div>
    </div>

    <div class="main-background">
        <div class="left-container loadingFade">
            <div class="left-container-handle"></div>
            <div class="top-left-container">

                <div class="filesystem-buttons loadingFade">
                    <img class="loadingFade" draggable="false" id="newFile" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAExklEQVR4nO2dTY8VRRSGe2EGXWgwGiPowmjUlUE0YEycQYhx5W8wuMEVuiCCO4WtBjJuUHZsXPkJIcSF7ojRGBy/SPgLIGCiprveM8Nr6k7HzDBdfT+qu6tO3TpJream+q2nz5yqU3Xq3qLIli1btmzZsmVTYyTvJvA2RX4g8A9FGKwBhiKXCOwtUjKSj1Lkl6BwpRF4SZFXi2Q8OUbIkhjsOlyEByqJwx7F5NAgZQ5gE/g7MqD/Jgk7OFjZAnOx9eUDFUVeK7RZcLCyuY00pQg7RtBJwo4VdHKwYwadFOzYQScDWwPoJGBrAa0etibQqmFrA60WtkbQKmFrBa0OtmbQqmBrB60GdgqgrVFk/9gt1pBnkKHB8s5G7uwNtsilbulNJy48XNnkecc8x+OGDZjuyE0vLDxc2QzDwu7Ls7ulN50ozlMrMmjJoEN7IbNHS3BwOXRIeKg5RksGHdzjmD1agkPKoUPCA8wxWuJqOWGRDDq4FzJ7tISDBqxRZIUiywQOUeRlluXjJO8nuUByG8mHWFVPUuQAgbcociaHDpkQLvAdjTlI8oFCkykBXFHktPXYQqtFDvg2gbM+e9PRWHCY4mxXCSwVqViknvwZye1FShZhqDgysXa7srDHViInCHxJkSsEbhJAfSR2kyJ/1H87PlqZkNv6JeoSGw9k4erq6xNpBp63SzUCf83wnFsU+YTGPNc/3Y2iY/Hk1fGQLRwC33T43Is05tl5An2kVSN5T52YrPbynyRyyl7VThs08Gmrvqp6miK/DqBlxWaRqYK+SvJepzbgBQJ/DvjSr/dWNhZ4hbE0BvLw16ftM/uAHRD02dZwMaQnN3l212Ek0EBKV1pdT3xDxORxbaXTCTLQIE636Fn2eIE2SXmH5I5RA47WXxs0q86TekEDa65duHqdPPsSDji6pU9bMDl7f0JjdmkF/a1Ti28yQu7Y0if5sKfeCzpBG3OwJa326ruXMdrVkTG7dYEGbpN80KHjTJSgx8wpcYIW+dm5CzfLBtFQoO0uILmgCfSyQ8P+LvrvdYzAPj2ggUMODSeiBy3yvibQ+xo1AF9HDxr4Qg/osnzMoeHKNMmI14A3Pne6pOZ3PaDZXIsx0b5GQzLSlU2U1ADXNYFecAx0vEd16MkzJTVApQn0XR6ge6vtIPlIaqDv8wgdXjdqWxkA76YVOkrvydDrRu2W55I7R30mNxkCLzVqAL7qov9exwh8rge0MW84NBxXAPo9PaBFPlKcgi9qAv1Ty6bSrWhBAzd0bSoBa3mbdDjYbzqPseLd+PcvGwtQO/Fji5aLXn03LP0mSkbaQZ/3hhzsxxRM84Gn9Zy6Fm5WKMdmSkbaD2ef6Qb0+m2lmMoNTnmA+T+pmTIZcbUPOoG8oZh7ZVDQgGFVPdXyAzzD6mlulzuvMK1/wmlo2OeceuzdQFuWFQoycI1l+USnkO9Yyx6myPcDTpCvOPUAewMWOe4p5skI7Bl513CQbxB4sZhH4/oV4yHC2uXewoUW4/oEedJr6ef2Ytvnh71frdBkNGaXrYUbZWvdFMKf72ydnKLRmN0U+bi+Rzh9HLb3yoe6jZWC0X5dBLBki1ts3YU9BRkdi60nLrbZI7Lf7KZ9/ZlFn124/wBxdyCcb06LmQAAAABJRU5ErkJggg==">
                    <img class="loadingFade" draggable="false" id="saveFile" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACD0lEQVR4nO2cMU4cQRQFfwRIcALgDJCBD2VDiENChwuHAhEZn8EnsLAERIXGGlnWyqyY2em3f/+8ipG6XtHqzSbCGGOMMcYYY4wxxgSwB1wCD8BvPkA0YOhZK/Su0/1bgWPgx0fiblHoXLH7mzw4ckcjn/8y9O/Txe6fi1HEdoTOEbt/k6uH3nxs4ImRRBufQWcNVP4Wm2Js5A6lz4T+m4k9QvQvSp+J/fWxR4r+QenTwF8be8ahtbFZgxD6tPCXxl7HMIQ+LfylsdexC6FPC//WWyYTDaFPC//WWyYTDaFPC//WWyYTjQQ4tAiHFjGL0MBhc8HV7kdzCX3VXHC1+9e5hH7tYqtvdndef253/iQopA0OLcM3WoRDi3BoEQ4twqFFOLQIhxbh0CIcWoRDi3BoEQ4twqFFZA79DCyAM2C/uej7/vvAOXADvFQL/RM4iWQAp71bidDPGSMvxR58sxViQ1lEcoDbCqHPIjnApwqhDyI5nePWh44tgWy70glV3ZVOqOqudEJVd6UTqrornVDVXemEqu5KJ1R1VzqhqrvSCVXdlU6o6q50QlV3pROquiudUNVd6YSq7konVHVXOqGqu9IJVd21zufYCvEr9QcGC3GvCH2x6ZUJ+KwIvQs8Ml++AzvNQ//zWePHmUY+kkReutlfuveq+A/kE3DXPReym2yMMcYYY4wxxhgTuXkDb/0B3KqLFqEAAAAASUVORK5CYII=">
                    <img class="loadingFade" draggable="false" id="saveAll" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACY0lEQVR4nO3cPW7VQBiF4REgQApsIFAjKugCS4B10PJThpKSMvxshIYlgKgIWwAqOgRSoHrRgIVQZBvPeObcsX2eerjz+Y3joMnNDcHMzMzMzGyLgIvAI+Ad8J0JZu6X9JojYzwJSwFcBT5MifuvmXv2Sl2/mNjdnZwcOZq5b6/U9YuJ3T0usoS2Qrcdu3smryV0u7GBb2QK8/ZNes3E0Z6G1uRGjmrsW3DOtmJnXMBfNfYtPGc7sTMv4Lca+1aYs43YuwqtnLOJ2BsJvfvYzBAWMmfV2KfPLipdwH7xwftn3C8UmupnFyNr5zgsOvjwjI8ppPrZxcj6OX7G2LXu7O5OPuz2KaL62cXI+k0Jtc8uHLp86N6zC4cuH7qXQ//h0CIOLeLQIg4t4tAiDi3i0CIOLeLQIg4t4tAiSwx9AhwBB8BesQsYnnMPuAU8A37kDl1yoKQNMuf9BNwIOwLc7GZYdeiTXUY+FTv5zl5S6KPQCOD5mkMfhEYAt9cc+lJoRJxltaFDYxxaxKFFHFrEoUUcWsShRRxaxKFFHFrEoUUcWsShRRxaxKFFHFrEoUUcequhh34FNeeDURboqyL0tdIf9bNAbxWh7wysf8h23FeEfjGw/gJwzPq9B84rQn8Ezo78kf7xyiNfKRb5P6GjeyP/Lt7ZD+JzbCU/IOM1vImPi6J38sTQn4HLxTfdoglf6ddDjxBLMPHbKr7H+EzK61pe6OiVHyOa0NGX7oNUzs3Zc5PIE989/xK4C1xv6R2jzVrJf830ZxcZoX12oeCzCxGfXQj57ELIZxdmZmZmZmZhfX4BCA6DqXhR6dwAAAAASUVORK5CYII=">
                    <div class="spacer"></div>
                    <div class="undo-buttons">
                        <img draggable="false" id="undo" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC1UlEQVR4nO3cz4uNURzH8S8ZimwoIqykyJ6bv4CEsBUri8kCGylTiH+ADJaSv2CSjZ9rtmOUO9lJzSS/Fn7OW6f73NwmwzzPzD3ne879vHazO/c9T+c59zznuWYiIiIiIiLyB3Cx50/pV2QA1Y0QOVDoCJEDhY4QOVDoCJEDhY4QOVDoCJEDhY4QOVDoCJEDhY4QOVDoCJEDhY4QuY++Ae+BNvAYuAWcAnYCS7L+5zqK/D/vgNvAnuyiZxR5tgngBDBk3mUcudcb4Ih5VUjkXg+ALeZJgZG7PgBHzYuCQwczwIh5UXjs4Dqw1DwAzlG2UfNiAK7sC+ZF4Vf2DHDQvCj8yp4GNpsXHjaVgCFgHbALOF3td/xYhNj3zROP26TAGuAS8HmBsQ+bJ143/oH1wJ0FhJ4Elpkn87lBWrqxnQS+N4x93Lzx/HAW2N9w7n7pcov1X1e2pR9buFk20TKPPB+gAe42CH3TvOIvV7Y5UC0FPzV4UuNv+pgrtjkBXG5wVe8wz3B4bBdY2+DGOGzeUV3Z5gjwpGboG5YDnL1aAZypGfpR6jFnCWjVDD2ZesxZovP1vI6p1GPOErCiZuivqcecJRQ6Dk0dkehmGAlwtuYcreVdE8CzIr+weFLsV3BvgKvUtz31uLMCbAC+1Iz81vU2qUfAvayPihW60ujanXrs2QAOAD+pbzz12LNB57hB09NLx1KP3z1gY8M5uavt7gCNw3XylQari9kOpf4sbgDLqw2iVnWze9pwLp5tzEoFrKpivQA+ks4UsMlKBGyrjl95OIi+10oErAZe4cN5KxUwgg9l79DRWUalds3N6299fHb3K/GcXO504SR0eClonw0K4HWCyGPFLuHmEl6ijBi47eo9wgTLu4k+Bx4PG0QDv3cBbK1iLKbwZGTU7asRqQArq/dMnle/pTHfH6+arub5h1XYYfcHx0VERERERERERESseL8BBy3/MpQdp94AAAAASUVORK5CYII=">
                        <img draggable="false" id="redo" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC2ElEQVR4nO3bTW/NQRTH8SFKQiwQDxssWAnrK3gFggWJrbAUlJWFJvey6o5EPHXT8B6EBbUXO9E2qWCHBJHopi6+MjE3uWkl7cxtZ86Z//m8gnN/d3L+8+icMcYYY4wxxhgZgNHSNTQC/1jYmYK2sDMGbWFnDNrCzhi0hZ0xaAs7Y9AWdsagLeyMQVvYGYO2sDMGXU/YwCrgAHARuA9MAG+Bb8AcMnSc4nCPAGPAZ3TQEzYwBJwFptFJftjAaeAD+skMG9gNPKUussIGTgBfqdOok8D/68Af6tUpHfBq4A516xQNOQR9i7q1pbSLmnUkhHys8p7cljKF80vmWnWcBMs0T+4Cz4FhoAVs8yvJFapXZch+xTeIH6G3b8pYs7qQhwZcVo/7kVugbj0he8C5xIB/AVcL1i3/wzdvq3M6sRcfLVy7jpHshf3kFBcE1C5/JPeETftY404AFSO5r218SphdbHcCqBjJXjjji9V2QkitawHfZyND/plznrwY0e2iXzitjvHMCSJ+JPcALyKDHnaCiB/JPcD7yKBbpWtWCfgSGfTW0jWrlHCDaG3pmlWyoDOx1pEJ8C6ydbRy1VaVcOMzxuXSNauUsGCZKF2zSglL8C6wuXTd6gD7iXe9dN3qhG3Sj5FBzwI7SteuDvAgYVQ/LF23OsBh0lwqXbvG9jGVEHTXXx8rXb8q4T2KuusG6oQLNLFbpv0e2Qdy6WGfYjCzwA1gy8oOiwoATxhcN5zcXAEO+hNz215dGPSuwo+CvgOvwp+0wdUMOC7kIvobYK+rGTCCDFPARlcz4CYyjLiahedvt0unDMy4JghtpGTP/g2sc00QXmrFXk1YLs0J2gN2Ao/JrxmtYz7gZMKh7iCuuaYC1gBngMkVDnmy+undUgGHgHsJJzWLeQ3sKf37RAL2AeeBu+FR50z4iM5FLMFfhseg60v/HmOMMcYYY4wxxhhjjDHuf/4CUwgDGss7Nn8AAAAASUVORK5CYII=">
                    </div>
                </div>
            </div>
            <div class="bottom-left-container">
                <div class="folder-header">
                    <img draggable="false" id="folder-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACXklEQVR4nO3cv04UURTH8aFCrEQSYmGhBJ5ALXgC18Q30DcwiIWWoNFnUB6BBDp6bUz804lWSiXEB4AlYtyYr5nkFhsh4xnmzrk7c3+fF7hnvplsZg/sFIWIiIiIiIiISKaAC8Aq8BE45vz+APvAJrCc+romCnAV2G0Qtyr689TXN0l3chuRxz0ochc+Ltp2AiwUOQufyR52ipwBQ/zcLXLlGHnSlU9aH4CHwLRC+/hUPonpjvaLHe/Odhq6q1YU2sd7hfYxVGgnCu1EoZ0otBOFdqLQThTaiUI7UWgn0bd4IiIiIvEAM8AzYA8YeT0i9cAoNFsv/+HIEvld6ol74G3Zsir009QT9shaVejy1pc4vlaF/hXpEIGfuqN9fKsKveE0RA5eVYW+k3q6HhlUhZ4GjlJP2ANDy7P0duope2CrMnIIfT/1lD1wzxL6sr56N/4qPvff0CH2m2ZnZe21KXII/Sj1tB22Wif0tdTTdth1c+gQ+3PqiTtot1bkEPpF6qk7qP4vgIFbqafuoJvnCT0FHKSevEN+lM1qhw6xtWSKsUQyhB7UOCh3t5uE1pLJvkRq9ntDLZkiLZEMobVkirFEMoS+BPw2HJbzEmm2cegQW0umGEskQ2gtmWIskQyhtWSKtUQyxNaSKcYSyRBaS6bT4r9GrlyYnHFQ7m60EVpLplhLJENsLZliLJEMobVkirFEMi6ZDscOy9VhK69j+ye2Pj7gZauRQ+grmf/lZR+Ybz10iL0UDszNd2DRJfJY7IvAE+BLeFNuX52Ea3xcXrNrZBERERERERGRYjL9BcEs+3kWPNUUAAAAAElFTkSuQmCC">
                    <span >scripts</span>
                    <img class="folder-arrow" draggable="false" id="folder-arrow" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAABVklEQVR4nO3aPU7DQBBA4SUFUHBwqIhEH+5AEXEiOABCKR8y8jaAkA3Z8f68r4wsZebFdiwlKUmSJEmSJEmSJEmSJEmSFAu4Au6AV+AFuJ1e83M4b+RL4InvnoFrY5eNnBk7IHJm7IDImbEDIhs7MHLmmb3wEe7I744Lj/HR7x9n8ufZuubYH99sVPwhnLEDImfGXogz3AKMHRA5M3ZgGPyCjAti7MAQw8cm8NIeNjYbLD5c7C0XZpTYNSxKBTMUVdOCVDRL94tR4UzdLkTFs3W3CA3M2M0CNDRr84PT2szNDdzi7M0M2vIO1Q/Ywy7VDtbTTiv+EtDcz/3UtBvwUMUg28belx5iB7z3GnlF7DfgIhUOfeo58sLYU4NdKgl47D3ygtiHVBpwM8c+zZfQfY+Rv8Tez7tOOx+mBilK0XtUhaZ9R9tZkiRJkiRJkiRJkiRJUmrMB8iTOG5Bg5VCAAAAAElFTkSuQmCC" class="collapse-icon">
                </div>
                <div class="files-container-wrapper">
                    <div class="files-container loadingFade">
                    </div>
                </div>
            </div>
        </div>
        <div class="main-container">
            <div class="actions">
                <div class="action-buttons">
                    <div id="execute" class="loadingFade"><img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACLUlEQVR4nO3dMYoUQRTG8RZRERQ2EQ011sQLeItNDb2CeIMVFTHcK3iF3guMuRNPMGuwywTiJj3g/E16QBBl131Vr96r73eCqo+G7q/7FT0MIiIiIiIiGQG3gbfAN+Ac+Ag88F5XOsARf/oOvAHueq8vjflK/ps18Aq46b3O8LicJXDovdYegt4bgefeaw6Jq9sBn4En3mvPHvTeBHwCDrz3EALXtwFeA3e895I96L0V8BK44b2nJmFvAbzw3lcPQf/+hPLMe3/NoKwtcAw8HHpHHRdz1b8/9Iq61t1Wenwsu6v0+DrpptLjb9dFpacdU+pKT3s2KSs97VqlqvS0b5Gi0hPHGLrSE8t2rvSPhmiI6SJcpSe2dZhKTw7L5is9uZw0W+nJZ9dkpSevqalKT36bJio9/Vi5Vnr688Wl0tOvsWqlp2/befD+loKu472CruNcQdehoCt5pyu6/M3wg26GZenxrjAVlsJUwQvTS6XC9Jq0ML34r0CfsgrTx9nCNG5QmAZoCot7yos4Rg05lqWx3cI0iN5FZbZGO6amJouseadLq5XZmnPIY7PTn9acAl42P89srXLA6zAT+tYqBfxjPnNyb+hV4YC3YSuztcI3uqfe+2tGgYAXKU66WjMMeJXq7LY1g4A3KSuztWsEPKWuzNb+I+Cfc2V+7L32UK4Y8thNZbZ2yYC/dleZrQGn/wi438psTT9TqPt7kKP5yj7T70FERERERESGeH4Ba6DZnW6HaMEAAAAASUVORK5CYII="><span>Execute</span></div>
                    <div id="clear" class="loadingFade"><img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC4klEQVR4nO3dQW7TQBTG8VmQFrIBLgZh1XIStpXgAqwQJRJnANGmHIJCWSFRwYr2FC9/ZDtVSRsSJ43nvXl+n2SpUltp5qdPiT0ZxylFIpFIJBKJRCKRSCRPgAHwDJExIt8QuUDkcvbzuP4dDDINx2eAfUTOmU5ZelR/A/va4y0uwD1EXq8Evg1+COxoj7+IALuIHK2NfI09Ae5rz8N0gB1EPm6MfI39GXigPR/fyNPAzocc2BmRAzsjcmCnfMh9xiY3ch+x0ULuEzbayH3AxgqyZ2ysIXvExiqyJ2zuukCUD3tS7Kof1pt8G/t9Ki2U0uSbBzxPpYTSmjzf6t9FvIRQapPnWz1KlkPJTZ5v9TgZR/6gjrQd6NNkMXhCbqAvk7XgDbmBvkiWgkfkBvpLshK8IjfQh8lCXJzCTZcc8FTb2HeTp3Wbf6lfsMya/GnFQI8ReVlwm/fsN1nk5GorFvCiwDa/KaPJzO93Q+SgIGTdZdJ1m3wzRTR7yfiLQC4C2wuyaWxvyCaxvSKbwvaObAK7L8iq2H1DVjnPNoA8aHEx0tnNN+TAtnDzUHXZ2WIXT6eDpEts7SbXE4Q9K02gC2wTTW5umPyh2eROsS00uZ4UPLHYBLaBbaHJV6lv5V08yO/AUHlsBy6Qq1QfQFrepcMm2NaQqyDy5z/Qj5KRsA62ReQV0I+ToSDyqljkEl46Wn/abhl5xZvhmfaboRvkKtXehSUTOKomqji2XRfI/6xxnFs74afN1l8rFyNbvATP2mw8NXmDRaUs7cFjkxdMcKLZbDw32Uqb8N5kCxOmb8gaE6evyDkB6DtyDggCuXsQArl7GAK5eyACuV0qxHqj+eqN6MMF/zvsxcVIZuyzelUQHs6OUf0ZZCCrf0nrSTS5a2wJ5LaLQMd3QI7X5AxfDf9W/YZJ5w87+Kl+s6STx3eMEHmHyNfZ4zuq43T2cIPqTCQe3xGJRCKRSCQSiUQiKVP+AmTgs+tI8fSDAAAAAElFTkSuQmCC"><span>Clear</span></div>
                    <div id="console" class="loadingFade"><img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACQklEQVR4nO3awU4TURTG8dGFlAVvwDPiY5CyMYoLXOkzmCA8AuzgIawkLkxsUTff+cyUWVSgpdg7554z/f7JXXaY+eX2TGmnaZRSSimllFJKKaW2NJIjkq8JXBKY0YxbtYAZgQuSByR3+kLeJ3Bd/WItyGotyP3SyCMh22PYV0V39nxc1N5BFnSRB+Wg25lc+4Is6AIuSkJPq1+QBV3AtBx07Yux4It8IWgTNKvvRO1oq4+n0WH1YTWjTdCsveu0o60+lEaH1UeMMKObLYuACdohQTslaKcE7ZSgnRK0U4J2StBOCdopQTslaKdCQ5PcJfChe5zqO4Gj3h6n2mroFtnuvRb4khE7LHR7AkufCUE+7LDQ3cn9XPo9bjLs6NBvVn5pngg7NjS5M8ccAHZo6PnryVcEPj+Bfd4+HtwELjz0ULBTQA8BOw109pmdCvoZ2IdNsNJBrzVGgJsmWEOF/toEKx00NTr6h+Z6yGe6GerjHUOPDib/DJ1iRnMAyOGhu5l8usZMHq3xS817Aj9WHus5qz1We0xyNz808G5T5O44J8WAH57DSWpoki8J3G6MfHecXz1C37Z/Izv0702QF44j6JVIwMdNkBeOo9HxxG7cI/CJwJ/ukYO3//PPSHczPO7hZng8iJvhP29/FjqhSqWAHkKCdkrQTgnaKUE7JWinBO2UoIcOrWWCpudG0I62ZNDARGPCln0x9a0Icgc9FrQtgx6Xg777cXWsnW2LwJO5ScCHMZVSSimllFJKKaWanvsLcUUQHAHImrwAAAAASUVORK5CYII="><span>Console</span></span></div>
                </div>
                <div class="status-holder">
                    <div id="attach"  class="loadingFade"><img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAADZ0lEQVR4nO2cO4wNURjHP494S4SEREUiIhoRUYmIQiUKKqGg0KMiGo2g8IrnolDSErtREaUSQRCJ1wqJZ7yC/e9PZu8mi7XMvXfOzLlnvl9yq5ubO+c3//nOzJlvxsxxHMdxHMdxHMepDmA80iGkt0i9SHuBcRVuUpognaS/n98+Une2A6retmQAViH1DxPdkH0FmFD1NnY8wDSkZ3+V7LKLA+n8PyW77PYB1uaS7LJbB5iJ9Kop0V6zmwfpctOSXXZzAFtaluyy8wHMQfrQtmgvIyMDjEa6Vohklz0ywPZCJbvs4QALkL4EEe1lpAEwFulGMMkuuwF9fbuDS667bGAx0vfSRNdRNo015lulSq6jbKQDlUiuk2xgOZIqFd2Q3ZPszQNgCtKjyiUPyd5nKYK0p3K5v4vutRQBZiHdiUj0a0sVYpItHbSUIQbZUlc0bQvAJGAd0hGk60gvkD4Pbug7pPtIl4BdwNKOkJ2NAVZbRAs9Z5E+NjmIh8C27OwiStnSBWBGeIP/H/j0gUOq3fNc6SWwGRgVhWzpDbDeYgBYgfS84AFeypOgoLIbXU2zLQaAjcEWeKRHwLycd79vF/i/n4GteY6q0kA6FfjQ7QXml5bsbOKGuRYb2V5HOh5Y9ktgYdBkS1+BHcAYi5WOly3dBBZZJzAo+0RHyZZ+IO2P5uIjSdnS3WYvlKIietlSP9JpYLJ1OtHKlh4DKy0lBmWfjujUbx8w1VKEiJKdPJSX7PguMhKV/SCK1bWalJHuqNYnKpZ9Jqhs2FT1OOshWwOTY66bB3WRfTZgqrdVPcaY+ud6Qk6MVncILXko1UusrgDjBm5RhZbcEL3T6ghlJXmofFy0ukEeydn3RU6Q0j2rE+QpF4M9x4Ve1EjvrS6QN8m/9BoXdp4t9VkdaCbJNvy37Sdb+mSp00qSC1+Ikp5ayrST5EKTLV21VClSctuypQOWIkWUi0LLCKyx1AiR5LaSnb1SAiZaSoRMcsvJlrosJcqUnFt21n2UowO1YyijXLTU6ycdtVSoIskjyO764z+fZC8XtBSIQfJfZUvfgGWWAjFJ/kP2KWCDpUCMkpME6ZhLLueVZ42HMT3JwUV/dcklgHTOa3J5LyY5N5Ds7PFj6bBPfAHxJkLHcRzHcRzHcRzHcSw+fgIhCpbOR6lhggAAAABJRU5ErkJggg=="></div>
                    <div class="holder loadingFade">
                        <span>Status</span>
                        <div class="status loadingFade"></div>
                    </div>
                </div>
            </div>

            <div class="tabs-wrapper loadingFade">
                <div class="tabs-gradient-wrapper">
                    <div class="tabs-container"></div>
                </div>
                <img draggable="false" id="newTab" class="loadingFade" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB1klEQVR4nO3byUoDQRRA0ezirP/g9HkOIILDQvDrVNw4G8FPMIIuw5U2DQ5E7YaOlXp9D2STTV5f3qIDVZ2OJEmSpPCAaWAq9RwhAUvAMfDIhwfgCFhMPV8IwPq3wN8VwddSz5k1YA7o8bc7YDb1vNkCdqluJ/W82QLOa4Q+Sz1vtoDXGqFfUs+bLWpKPW+2MLShQ8GNNnQouNGGDgU32tCh4EYbOhTcaEOHghtt6FBwow0dCm60oUPBjTZ0KLjRhg6Ftm50cb4N2C5OBQHPtE+/fPatsZ31K05sAtepn3SCXAEr4zjVaeTRp1ibO58NHI74EQ0dNBm6OOyt0XpNRe4Cgx9+RLy36Ro6l9DlVle53tBWvUYil6EPUj/NBNtr+vWueG/UV7fAQmOhy9grxv7iAlhuNPKn2DPAJnBa/h1tmz5wAmwULTpRUFPqebOFoQ0dCm60oUPBjTZ0KLjRhg4FN9rQoeBGGzoU3GhDh4IbbehQcKMNHQputKFDwY02dCi40f8Wul+j9dM/jRUPw4s5VZ2knjdbDG+AVbWRet7cr9tdVYh8GeosXArAKnDzS+TrsZ3qbBtgHtgvbx4Mys99+d186vlCYnh5qZk7I5IkSZI6k+wNJgs9CuOiKBgAAAAASUVORK5CYII=">
            </div>
            <div class="editor-container loadingFade">

            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.20.0/min/vs/loader.js"></script>
    <script>
        // init
        const imgIds = {
            "editor": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEQUlEQVR4nO2cTahVVRTHr0FKGpETDZvYpN5r4iCnfUBNNGqik1AqqEYZlHMNqlGG5sA0sEIhDQILaqQO8jWLoJFFk6Ampmj5WRHv7y/uuZfHq87e55zr/jr3rR9ceIN39lp7vf32f6+19rmDgWEYhmEYhmEYhmEYRnuAZR1+3egKsALpPaSrSH8iHQbu6DyQ4QdpHzdv8q+PdLDhMaMLwG1Iv9cE+kqngQw/wMz/gjwK9OWGR40uANsdgZ7rNJAxwf48CvTehkeNLiB9XRto2NZpIKNRCK86Aj3jedToAjDr2DauDf8InQYz3JgQJgITwmSBPuPYn7dPfc0EWI90Emke6RywI4MQzk445iqkD5D+GH8ODOsog9IYO/p9zcS3JMwIJxZCpPdrxjs8KA2kQ47JnwhuC7aFzgiRrjv+Q4IvlIkBnq51cjT5T4Pbk/Y6bO2b0P9lw0KUY8yLwL2h5zCJk/cgXXAGGp7sgxAi7fcsllNZz+bjlfCFx8EjfckIGWnMj54F81rYmXRzbocnyD8Bd/UpIwQeQvrbMf5fwIZwM2nv1Gx1DKp3SsCjiUujZwKNv8uzeM4mbZON+3TfeRx6o68ZIaOt6SvP3N4NYaedM9IejyPfArf3uTQK3Oc5hQyNbQ5ly+fEI1XmV+/EdeD+aSiNAs96FtN5YG1Ie/81fjfSzx5lfmGaSqNIxz3B/jy0vbaGP4tmOJEQTrCwXoxh9DlPkH8F1gQ3WkBpFHi4Yat8YDBV4jDI1yNEeju6+Lc47kxUX+hTj3AYSKRvPDF4M4SR3SUc4MncIxwnaDeiJGjAxlJSUhILocOHlz2L7hdgdYwiy6tRZlNwj7BFEe1ouImNBjyZurdGpB5hZz9gbZWwuBdgt4NBVfB2F8LXRZtJoh7hrQA8VZ226uNzrM+BnskphLEDXczWQYQeYcStY1NvxZAChDCaGJZ0vEOaK+HWaJTj3cLg8/Ov50xYKOTWaIuE5bEQE60/WiVIwSng1miLFPyt3heVKCEjbC4qLQ9nDJ7PUSYlsxAmLZMuGJU+SV34J6MQtij8vzQVrSwyC2G2Vtai5qxSNGfJKIRZm7MLTkjvpLhuQCYhbCH+we8TZr1AQ54eYVNHaX8s2y6HHox9JYwMQljUlbBFTr0S65IjGYSwyEuOi4osX8a4tkvqyzLNRbSdoW2Gvoj+RB9Ko8PLi54Fc7qIl0QbXq04UsLrEy3sXXLYu1TEqxUtXhY62oceobOjBFsHJTHe487WnD4e70OP0PGVQeW9/rZovz5R/btJPwDP9KVHCCyvgi39Vq3u4c8hq3IlQgGl0SUBhfQIpx4K6RFONfiFMHyRfalCAT3CJQEmhIkCLRPCVIGeMyFME+jLKTPCJQt1X1AyDL4JYfBAf1gT6AOBzRjAnUgfV52O0ecjYKVFJmYDmCkv6hiGYRiGYRiGYRiGMQjMP/4Yv/FE4HhAAAAAAElFTkSuQmCC",
            "settings": "data:image/png;base64,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",
            "incognito-logo": "data:image/png;base64,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",
            "newFile": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAExklEQVR4nO2dTY8VRRSGe2EGXWgwGiPowmjUlUE0YEycQYhx5W8wuMEVuiCCO4WtBjJuUHZsXPkJIcSF7ojRGBy/SPgLIGCiprveM8Nr6k7HzDBdfT+qu6tO3TpJream+q2nz5yqU3Xq3qLIli1btmzZsmVTYyTvJvA2RX4g8A9FGKwBhiKXCOwtUjKSj1Lkl6BwpRF4SZFXi2Q8OUbIkhjsOlyEByqJwx7F5NAgZQ5gE/g7MqD/Jgk7OFjZAnOx9eUDFUVeK7RZcLCyuY00pQg7RtBJwo4VdHKwYwadFOzYQScDWwPoJGBrAa0etibQqmFrA60WtkbQKmFrBa0OtmbQqmBrB60GdgqgrVFk/9gt1pBnkKHB8s5G7uwNtsilbulNJy48XNnkecc8x+OGDZjuyE0vLDxc2QzDwu7Ls7ulN50ozlMrMmjJoEN7IbNHS3BwOXRIeKg5RksGHdzjmD1agkPKoUPCA8wxWuJqOWGRDDq4FzJ7tISDBqxRZIUiywQOUeRlluXjJO8nuUByG8mHWFVPUuQAgbcociaHDpkQLvAdjTlI8oFCkykBXFHktPXYQqtFDvg2gbM+e9PRWHCY4mxXCSwVqViknvwZye1FShZhqDgysXa7srDHViInCHxJkSsEbhJAfSR2kyJ/1H87PlqZkNv6JeoSGw9k4erq6xNpBp63SzUCf83wnFsU+YTGPNc/3Y2iY/Hk1fGQLRwC33T43Is05tl5An2kVSN5T52YrPbynyRyyl7VThs08Gmrvqp6miK/DqBlxWaRqYK+SvJepzbgBQJ/DvjSr/dWNhZ4hbE0BvLw16ftM/uAHRD02dZwMaQnN3l212Ek0EBKV1pdT3xDxORxbaXTCTLQIE636Fn2eIE2SXmH5I5RA47WXxs0q86TekEDa65duHqdPPsSDji6pU9bMDl7f0JjdmkF/a1Ti28yQu7Y0if5sKfeCzpBG3OwJa326ruXMdrVkTG7dYEGbpN80KHjTJSgx8wpcYIW+dm5CzfLBtFQoO0uILmgCfSyQ8P+LvrvdYzAPj2ggUMODSeiBy3yvibQ+xo1AF9HDxr4Qg/osnzMoeHKNMmI14A3Pne6pOZ3PaDZXIsx0b5GQzLSlU2U1ADXNYFecAx0vEd16MkzJTVApQn0XR6ge6vtIPlIaqDv8wgdXjdqWxkA76YVOkrvydDrRu2W55I7R30mNxkCLzVqAL7qov9exwh8rge0MW84NBxXAPo9PaBFPlKcgi9qAv1Ty6bSrWhBAzd0bSoBa3mbdDjYbzqPseLd+PcvGwtQO/Fji5aLXn03LP0mSkbaQZ/3hhzsxxRM84Gn9Zy6Fm5WKMdmSkbaD2ef6Qb0+m2lmMoNTnmA+T+pmTIZcbUPOoG8oZh7ZVDQgGFVPdXyAzzD6mlulzuvMK1/wmlo2OeceuzdQFuWFQoycI1l+USnkO9Yyx6myPcDTpCvOPUAewMWOe4p5skI7Bl513CQbxB4sZhH4/oV4yHC2uXewoUW4/oEedJr6ef2Ytvnh71frdBkNGaXrYUbZWvdFMKf72ydnKLRmN0U+bi+Rzh9HLb3yoe6jZWC0X5dBLBki1ts3YU9BRkdi60nLrbZI7Lf7KZ9/ZlFn124/wBxdyCcb06LmQAAAABJRU5ErkJggg==",
            "saveFile": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACD0lEQVR4nO2cMU4cQRQFfwRIcALgDJCBD2VDiENChwuHAhEZn8EnsLAERIXGGlnWyqyY2em3f/+8ipG6XtHqzSbCGGOMMcYYY4wxxgSwB1wCD8BvPkA0YOhZK/Su0/1bgWPgx0fiblHoXLH7mzw4ckcjn/8y9O/Txe6fi1HEdoTOEbt/k6uH3nxs4ImRRBufQWcNVP4Wm2Js5A6lz4T+m4k9QvQvSp+J/fWxR4r+QenTwF8be8ahtbFZgxD6tPCXxl7HMIQ+LfylsdexC6FPC//WWyYTDaFPC//WWyYTDaFPC//WWyYTjQQ4tAiHFjGL0MBhc8HV7kdzCX3VXHC1+9e5hH7tYqtvdndef253/iQopA0OLcM3WoRDi3BoEQ4twqFFOLQIhxbh0CIcWoRDi3BoEQ4twqFFZA79DCyAM2C/uej7/vvAOXADvFQL/RM4iWQAp71bidDPGSMvxR58sxViQ1lEcoDbCqHPIjnApwqhDyI5nePWh44tgWy70glV3ZVOqOqudEJVd6UTqrornVDVXemEqu5KJ1R1VzqhqrvSCVXdlU6o6q50QlV3pROquiudUNVd6YSq7konVHVXOqGqu9IJVd21zufYCvEr9QcGC3GvCH2x6ZUJ+KwIvQs8Ml++AzvNQ//zWePHmUY+kkReutlfuveq+A/kE3DXPReym2yMMcYYY4wxxhgTuXkDb/0B3KqLFqEAAAAASUVORK5CYII=",
            "saveAll": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACY0lEQVR4nO3cPW7VQBiF4REgQApsIFAjKugCS4B10PJThpKSMvxshIYlgKgIWwAqOgRSoHrRgIVQZBvPeObcsX2eerjz+Y3joMnNDcHMzMzMzGyLgIvAI+Ad8J0JZu6X9JojYzwJSwFcBT5MifuvmXv2Sl2/mNjdnZwcOZq5b6/U9YuJ3T0usoS2Qrcdu3smryV0u7GBb2QK8/ZNes3E0Z6G1uRGjmrsW3DOtmJnXMBfNfYtPGc7sTMv4Lca+1aYs43YuwqtnLOJ2BsJvfvYzBAWMmfV2KfPLipdwH7xwftn3C8UmupnFyNr5zgsOvjwjI8ppPrZxcj6OX7G2LXu7O5OPuz2KaL62cXI+k0Jtc8uHLp86N6zC4cuH7qXQ//h0CIOLeLQIg4t4tAiDi3i0CIOLeLQIg4t4tAiSwx9AhwBB8BesQsYnnMPuAU8A37kDl1yoKQNMuf9BNwIOwLc7GZYdeiTXUY+FTv5zl5S6KPQCOD5mkMfhEYAt9cc+lJoRJxltaFDYxxaxKFFHFrEoUUcWsShRRxaxKFFHFrEoUUcWsShRRxaxKFFHFrEoUUcequhh34FNeeDURboqyL0tdIf9bNAbxWh7wysf8h23FeEfjGw/gJwzPq9B84rQn8Ezo78kf7xyiNfKRb5P6GjeyP/Lt7ZD+JzbCU/IOM1vImPi6J38sTQn4HLxTfdoglf6ddDjxBLMPHbKr7H+EzK61pe6OiVHyOa0NGX7oNUzs3Zc5PIE989/xK4C1xv6R2jzVrJf830ZxcZoX12oeCzCxGfXQj57ELIZxdmZmZmZmZhfX4BCA6DqXhR6dwAAAAASUVORK5CYII=",
            "undo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC1UlEQVR4nO3cz4uNURzH8S8ZimwoIqykyJ6bv4CEsBUri8kCGylTiH+ADJaSv2CSjZ9rtmOUO9lJzSS/Fn7OW6f73NwmwzzPzD3ne879vHazO/c9T+c59zznuWYiIiIiIiLyB3Cx50/pV2QA1Y0QOVDoCJEDhY4QOVDoCJEDhY4QOVDoCJEDhY4QOVDoCJEDhY4QOVDoCJEDhY4QuY++Ae+BNvAYuAWcAnYCS7L+5zqK/D/vgNvAnuyiZxR5tgngBDBk3mUcudcb4Ih5VUjkXg+ALeZJgZG7PgBHzYuCQwczwIh5UXjs4Dqw1DwAzlG2UfNiAK7sC+ZF4Vf2DHDQvCj8yp4GNpsXHjaVgCFgHbALOF3td/xYhNj3zROP26TAGuAS8HmBsQ+bJ143/oH1wJ0FhJ4Elpkn87lBWrqxnQS+N4x93Lzx/HAW2N9w7n7pcov1X1e2pR9buFk20TKPPB+gAe42CH3TvOIvV7Y5UC0FPzV4UuNv+pgrtjkBXG5wVe8wz3B4bBdY2+DGOGzeUV3Z5gjwpGboG5YDnL1aAZypGfpR6jFnCWjVDD2ZesxZovP1vI6p1GPOErCiZuivqcecJRQ6Dk0dkehmGAlwtuYcreVdE8CzIr+weFLsV3BvgKvUtz31uLMCbAC+1Iz81vU2qUfAvayPihW60ujanXrs2QAOAD+pbzz12LNB57hB09NLx1KP3z1gY8M5uavt7gCNw3XylQari9kOpf4sbgDLqw2iVnWze9pwLp5tzEoFrKpivQA+ks4UsMlKBGyrjl95OIi+10oErAZe4cN5KxUwgg9l79DRWUalds3N6299fHb3K/GcXO504SR0eClonw0K4HWCyGPFLuHmEl6ijBi47eo9wgTLu4k+Bx4PG0QDv3cBbK1iLKbwZGTU7asRqQArq/dMnle/pTHfH6+arub5h1XYYfcHx0VERERERERERESseL8BBy3/MpQdp94AAAAASUVORK5CYII=",
            "redo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC2ElEQVR4nO3bTW/NQRTH8SFKQiwQDxssWAnrK3gFggWJrbAUlJWFJvey6o5EPHXT8B6EBbUXO9E2qWCHBJHopi6+MjE3uWkl7cxtZ86Z//m8gnN/d3L+8+icMcYYY4wxxhgZgNHSNTQC/1jYmYK2sDMGbWFnDNrCzhi0hZ0xaAs7Y9AWdsagLeyMQVvYGYO2sDMGXU/YwCrgAHARuA9MAG+Bb8AcMnSc4nCPAGPAZ3TQEzYwBJwFptFJftjAaeAD+skMG9gNPKUussIGTgBfqdOok8D/68Af6tUpHfBq4A516xQNOQR9i7q1pbSLmnUkhHys8p7cljKF80vmWnWcBMs0T+4Cz4FhoAVs8yvJFapXZch+xTeIH6G3b8pYs7qQhwZcVo/7kVugbj0he8C5xIB/AVcL1i3/wzdvq3M6sRcfLVy7jpHshf3kFBcE1C5/JPeETftY404AFSO5r218SphdbHcCqBjJXjjji9V2QkitawHfZyND/plznrwY0e2iXzitjvHMCSJ+JPcALyKDHnaCiB/JPcD7yKBbpWtWCfgSGfTW0jWrlHCDaG3pmlWyoDOx1pEJ8C6ydbRy1VaVcOMzxuXSNauUsGCZKF2zSglL8C6wuXTd6gD7iXe9dN3qhG3Sj5FBzwI7SteuDvAgYVQ/LF23OsBh0lwqXbvG9jGVEHTXXx8rXb8q4T2KuusG6oQLNLFbpv0e2Qdy6WGfYjCzwA1gy8oOiwoATxhcN5zcXAEO+hNz215dGPSuwo+CvgOvwp+0wdUMOC7kIvobYK+rGTCCDFPARlcz4CYyjLiahedvt0unDMy4JghtpGTP/g2sc00QXmrFXk1YLs0J2gN2Ao/JrxmtYz7gZMKh7iCuuaYC1gBngMkVDnmy+undUgGHgHsJJzWLeQ3sKf37RAL2AeeBu+FR50z4iM5FLMFfhseg60v/HmOMMcYYY4wxxhhjjDHuf/4CUwgDGss7Nn8AAAAASUVORK5CYII=",
            "folder-icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACXklEQVR4nO3cv04UURTH8aFCrEQSYmGhBJ5ALXgC18Q30DcwiIWWoNFnUB6BBDp6bUz804lWSiXEB4AlYtyYr5nkFhsh4xnmzrk7c3+fF7hnvplsZg/sFIWIiIiIiIiISKaAC8Aq8BE45vz+APvAJrCc+romCnAV2G0Qtyr689TXN0l3chuRxz0ochc+Ltp2AiwUOQufyR52ipwBQ/zcLXLlGHnSlU9aH4CHwLRC+/hUPonpjvaLHe/Odhq6q1YU2sd7hfYxVGgnCu1EoZ0otBOFdqLQThTaiUI7UWgn0bd4IiIiIvEAM8AzYA8YeT0i9cAoNFsv/+HIEvld6ol74G3Zsir009QT9shaVejy1pc4vlaF/hXpEIGfuqN9fKsKveE0RA5eVYW+k3q6HhlUhZ4GjlJP2ANDy7P0duope2CrMnIIfT/1lD1wzxL6sr56N/4qPvff0CH2m2ZnZe21KXII/Sj1tB22Wif0tdTTdth1c+gQ+3PqiTtot1bkEPpF6qk7qP4vgIFbqafuoJvnCT0FHKSevEN+lM1qhw6xtWSKsUQyhB7UOCh3t5uE1pLJvkRq9ntDLZkiLZEMobVkirFEMoS+BPw2HJbzEmm2cegQW0umGEskQ2gtmWIskQyhtWSKtUQyxNaSKcYSyRBaS6bT4r9GrlyYnHFQ7m60EVpLplhLJENsLZliLJEMobVkirFEMi6ZDscOy9VhK69j+ye2Pj7gZauRQ+grmf/lZR+Ybz10iL0UDszNd2DRJfJY7IvAE+BLeFNuX52Ea3xcXrNrZBERERERERGRYjL9BcEs+3kWPNUUAAAAAElFTkSuQmCC",
            "folder-arrow": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAABVklEQVR4nO3aPU7DQBBA4SUFUHBwqIhEH+5AEXEiOABCKR8y8jaAkA3Z8f68r4wsZebFdiwlKUmSJEmSJEmSJEmSJEmSFAu4Au6AV+AFuJ1e83M4b+RL4InvnoFrY5eNnBk7IHJm7IDImbEDIhs7MHLmmb3wEe7I744Lj/HR7x9n8ufZuubYH99sVPwhnLEDImfGXogz3AKMHRA5M3ZgGPyCjAti7MAQw8cm8NIeNjYbLD5c7C0XZpTYNSxKBTMUVdOCVDRL94tR4UzdLkTFs3W3CA3M2M0CNDRr84PT2szNDdzi7M0M2vIO1Q/Ywy7VDtbTTiv+EtDcz/3UtBvwUMUg28belx5iB7z3GnlF7DfgIhUOfeo58sLYU4NdKgl47D3ygtiHVBpwM8c+zZfQfY+Rv8Tez7tOOx+mBilK0XtUhaZ9R9tZkiRJkiRJkiRJkiRJUmrMB8iTOG5Bg5VCAAAAAElFTkSuQmCC",
            "execute": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACLUlEQVR4nO3dMYoUQRTG8RZRERQ2EQ011sQLeItNDb2CeIMVFTHcK3iF3guMuRNPMGuwywTiJj3g/E16QBBl131Vr96r73eCqo+G7q/7FT0MIiIiIiIiGQG3gbfAN+Ac+Ag88F5XOsARf/oOvAHueq8vjflK/ps18Aq46b3O8LicJXDovdYegt4bgefeaw6Jq9sBn4En3mvPHvTeBHwCDrz3EALXtwFeA3e895I96L0V8BK44b2nJmFvAbzw3lcPQf/+hPLMe3/NoKwtcAw8HHpHHRdz1b8/9Iq61t1Wenwsu6v0+DrpptLjb9dFpacdU+pKT3s2KSs97VqlqvS0b5Gi0hPHGLrSE8t2rvSPhmiI6SJcpSe2dZhKTw7L5is9uZw0W+nJZ9dkpSevqalKT36bJio9/Vi5Vnr688Wl0tOvsWqlp2/befD+loKu472CruNcQdehoCt5pyu6/M3wg26GZenxrjAVlsJUwQvTS6XC9Jq0ML34r0CfsgrTx9nCNG5QmAZoCot7yos4Rg05lqWx3cI0iN5FZbZGO6amJouseadLq5XZmnPIY7PTn9acAl42P89srXLA6zAT+tYqBfxjPnNyb+hV4YC3YSuztcI3uqfe+2tGgYAXKU66WjMMeJXq7LY1g4A3KSuztWsEPKWuzNb+I+Cfc2V+7L32UK4Y8thNZbZ2yYC/dleZrQGn/wi438psTT9TqPt7kKP5yj7T70FERERERESGeH4Ba6DZnW6HaMEAAAAASUVORK5CYII=",
            "clear": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC4klEQVR4nO3dQW7TQBTG8VmQFrIBLgZh1XIStpXgAqwQJRJnANGmHIJCWSFRwYr2FC9/ZDtVSRsSJ43nvXl+n2SpUltp5qdPiT0ZxylFIpFIJBKJRCKRSCRPgAHwDJExIt8QuUDkcvbzuP4dDDINx2eAfUTOmU5ZelR/A/va4y0uwD1EXq8Evg1+COxoj7+IALuIHK2NfI09Ae5rz8N0gB1EPm6MfI39GXigPR/fyNPAzocc2BmRAzsjcmCnfMh9xiY3ch+x0ULuEzbayH3AxgqyZ2ysIXvExiqyJ2zuukCUD3tS7Kof1pt8G/t9Ki2U0uSbBzxPpYTSmjzf6t9FvIRQapPnWz1KlkPJTZ5v9TgZR/6gjrQd6NNkMXhCbqAvk7XgDbmBvkiWgkfkBvpLshK8IjfQh8lCXJzCTZcc8FTb2HeTp3Wbf6lfsMya/GnFQI8ReVlwm/fsN1nk5GorFvCiwDa/KaPJzO93Q+SgIGTdZdJ1m3wzRTR7yfiLQC4C2wuyaWxvyCaxvSKbwvaObAK7L8iq2H1DVjnPNoA8aHEx0tnNN+TAtnDzUHXZ2WIXT6eDpEts7SbXE4Q9K02gC2wTTW5umPyh2eROsS00uZ4UPLHYBLaBbaHJV6lv5V08yO/AUHlsBy6Qq1QfQFrepcMm2NaQqyDy5z/Qj5KRsA62ReQV0I+ToSDyqljkEl46Wn/abhl5xZvhmfaboRvkKtXehSUTOKomqji2XRfI/6xxnFs74afN1l8rFyNbvATP2mw8NXmDRaUs7cFjkxdMcKLZbDw32Uqb8N5kCxOmb8gaE6evyDkB6DtyDggCuXsQArl7GAK5eyACuV0qxHqj+eqN6MMF/zvsxcVIZuyzelUQHs6OUf0ZZCCrf0nrSTS5a2wJ5LaLQMd3QI7X5AxfDf9W/YZJ5w87+Kl+s6STx3eMEHmHyNfZ4zuq43T2cIPqTCQe3xGJRCKRSCQSiUQiKVP+AmTgs+tI8fSDAAAAAElFTkSuQmCC",
            "console": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACQklEQVR4nO3awU4TURTG8dGFlAVvwDPiY5CyMYoLXOkzmCA8AuzgIawkLkxsUTff+cyUWVSgpdg7554z/f7JXXaY+eX2TGmnaZRSSimllFJKKaW2NJIjkq8JXBKY0YxbtYAZgQuSByR3+kLeJ3Bd/WItyGotyP3SyCMh22PYV0V39nxc1N5BFnSRB+Wg25lc+4Is6AIuSkJPq1+QBV3AtBx07Yux4It8IWgTNKvvRO1oq4+n0WH1YTWjTdCsveu0o60+lEaH1UeMMKObLYuACdohQTslaKcE7ZSgnRK0U4J2StBOCdopQTslaKdCQ5PcJfChe5zqO4Gj3h6n2mroFtnuvRb4khE7LHR7AkufCUE+7LDQ3cn9XPo9bjLs6NBvVn5pngg7NjS5M8ccAHZo6PnryVcEPj+Bfd4+HtwELjz0ULBTQA8BOw109pmdCvoZ2IdNsNJBrzVGgJsmWEOF/toEKx00NTr6h+Z6yGe6GerjHUOPDib/DJ1iRnMAyOGhu5l8usZMHq3xS817Aj9WHus5qz1We0xyNz808G5T5O44J8WAH57DSWpoki8J3G6MfHecXz1C37Z/Izv0702QF44j6JVIwMdNkBeOo9HxxG7cI/CJwJ/ukYO3//PPSHczPO7hZng8iJvhP29/FjqhSqWAHkKCdkrQTgnaKUE7JWinBO2UoIcOrWWCpudG0I62ZNDARGPCln0x9a0Icgc9FrQtgx6Xg777cXWsnW2LwJO5ScCHMZVSSimllFJKKaWanvsLcUUQHAHImrwAAAAASUVORK5CYII=",
            "attach": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAADZ0lEQVR4nO2cO4wNURjHP494S4SEREUiIhoRUYmIQiUKKqGg0KMiGo2g8IrnolDSErtREaUSQRCJ1wqJZ7yC/e9PZu8mi7XMvXfOzLlnvl9yq5ubO+c3//nOzJlvxsxxHMdxHMdxHMepDmA80iGkt0i9SHuBcRVuUpognaS/n98+Une2A6retmQAViH1DxPdkH0FmFD1NnY8wDSkZ3+V7LKLA+n8PyW77PYB1uaS7LJbB5iJ9Kop0V6zmwfpctOSXXZzAFtaluyy8wHMQfrQtmgvIyMDjEa6Vohklz0ywPZCJbvs4QALkL4EEe1lpAEwFulGMMkuuwF9fbuDS667bGAx0vfSRNdRNo015lulSq6jbKQDlUiuk2xgOZIqFd2Q3ZPszQNgCtKjyiUPyd5nKYK0p3K5v4vutRQBZiHdiUj0a0sVYpItHbSUIQbZUlc0bQvAJGAd0hGk60gvkD4Pbug7pPtIl4BdwNKOkJ2NAVZbRAs9Z5E+NjmIh8C27OwiStnSBWBGeIP/H/j0gUOq3fNc6SWwGRgVhWzpDbDeYgBYgfS84AFeypOgoLIbXU2zLQaAjcEWeKRHwLycd79vF/i/n4GteY6q0kA6FfjQ7QXml5bsbOKGuRYb2V5HOh5Y9ktgYdBkS1+BHcAYi5WOly3dBBZZJzAo+0RHyZZ+IO2P5uIjSdnS3WYvlKIietlSP9JpYLJ1OtHKlh4DKy0lBmWfjujUbx8w1VKEiJKdPJSX7PguMhKV/SCK1bWalJHuqNYnKpZ9Jqhs2FT1OOshWwOTY66bB3WRfTZgqrdVPcaY+ud6Qk6MVncILXko1UusrgDjBm5RhZbcEL3T6ghlJXmofFy0ukEeydn3RU6Q0j2rE+QpF4M9x4Ve1EjvrS6QN8m/9BoXdp4t9VkdaCbJNvy37Sdb+mSp00qSC1+Ikp5ayrST5EKTLV21VClSctuypQOWIkWUi0LLCKyx1AiR5LaSnb1SAiZaSoRMcsvJlrosJcqUnFt21n2UowO1YyijXLTU6ycdtVSoIskjyO764z+fZC8XtBSIQfJfZUvfgGWWAjFJ/kP2KWCDpUCMkpME6ZhLLueVZ42HMT3JwUV/dcklgHTOa3J5LyY5N5Ds7PFj6bBPfAHxJkLHcRzHcRzHcRzHcSw+fgIhCpbOR6lhggAAAABJRU5ErkJggg==",
            "newTab": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB1klEQVR4nO3byUoDQRRA0ezirP/g9HkOIILDQvDrVNw4G8FPMIIuw5U2DQ5E7YaOlXp9D2STTV5f3qIDVZ2OJEmSpPCAaWAq9RwhAUvAMfDIhwfgCFhMPV8IwPq3wN8VwddSz5k1YA7o8bc7YDb1vNkCdqluJ/W82QLOa4Q+Sz1vtoDXGqFfUs+bLWpKPW+2MLShQ8GNNnQouNGGDgU32tCh4EYbOhTcaEOHghtt6FBwow0dCm60oUPBjTZ0KLjRhg6Ftm50cb4N2C5OBQHPtE+/fPatsZ31K05sAtepn3SCXAEr4zjVaeTRp1ibO58NHI74EQ0dNBm6OOyt0XpNRe4Cgx9+RLy36Ro6l9DlVle53tBWvUYil6EPUj/NBNtr+vWueG/UV7fAQmOhy9grxv7iAlhuNPKn2DPAJnBa/h1tmz5wAmwULTpRUFPqebOFoQ0dCm60oUPBjTZ0KLjRhg4FN9rQoeBGGzoU3GhDh4IbbehQcKMNHQputKFDwY02dCi40f8Wul+j9dM/jRUPw4s5VZ2knjdbDG+AVbWRet7cr9tdVYh8GeosXArAKnDzS+TrsZ3qbBtgHtgvbx4Mys99+d186vlCYnh5qZk7I5IkSZI6k+wNJgs9CuOiKBgAAAAASUVORK5CYII="
        }

        async function handleLoadingFade() {
            const loadingElements = document.querySelectorAll('.loadingFade');

            loadingElements.forEach(element => {
                const img = element.tagName === 'IMG' ? element : element.querySelector('img');
                if (img) {
                    img.setAttribute('data-original-src', img.src);
                    img.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7";
                }
            });

            await new Promise(resolve => setTimeout(resolve, 3000));

            loadingElements.forEach(element => {
                const img = element.tagName === 'IMG' ? element : element.querySelector('img');
                if (img && img.getAttribute('data-original-src')) {
                    img.src = img.getAttribute('data-original-src');
                    img.removeAttribute('data-original-src');
                }
                element.classList.remove('loadingFade');
            });

            document.querySelectorAll('img').forEach(img => {
                if (img.id && imgIds[img.id] && img.src !== imgIds[img.id]) {
                    img.src = imgIds[img.id];
                }
            });
        
        }

        handleLoadingFade()

        // start
        
        const versionLabel = document.querySelector('#version_app')
        const editorContainer = document.querySelector('.editor-container');
        const tabsContainer = document.querySelector('.tabs-container');
        const newTabButton = document.getElementById('newTab');
        const attachButton = document.getElementById('attach');
        const executeButton = document.getElementById('execute');
        const dragRegion = document.querySelector('.drag')
        const newFile = document.querySelector('#newFile')
        const saveFile = document.querySelector('#saveFile')
        const saveAll = document.querySelector('#saveAll')
        const undoButton = document.querySelector('#undo')
        const redoButton = document.querySelector('#redo')
        const statusDiv = document.querySelector('.status');
        const minimize = document.querySelector('#minimize')
        const closeButton = document.querySelector('#close');
        const folderArrow = document.getElementById('folder-arrow');
        const filesContainer = document.querySelector('.files-container-wrapper');
        const consoleButton = document.getElementById('console');
        const leftContainer = document.querySelector('.left-container');
        const resizeHandle = document.querySelector('.left-container-handle');
        const infoContainer = document.querySelector('.info-container');
        const fileSystemButtons = document.querySelector('.top-left-container .filesystem-buttons');
        const folderHeader = document.querySelector('.folder-header');
        const fileWrapper = document.querySelector('.files-container-wrapper');
        const underline = document.querySelector('.underline');
        const topIsland = document.querySelectorAll('.top-island > div')

        const settingsContainer = document.querySelector('.settings-main');
        const settingHeaders = document.querySelectorAll('.setting-header');
        const settingCategories = document.querySelectorAll('.settings-category');
        const settingsButton = document.getElementById('settings');
        const settingsType2Buttons = document.querySelectorAll('.settings-option-button-2');

        const mainBackground = document.querySelector('.main-background');
        const settingsBackground = document.querySelector('.settings-background');
        const autocompleteData = {};
        const handles = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'left', 'right', 'top', 'bottom'];

        const orgDuration= {};
        let editors = {};
        let currentEditorId = 0;
        let activeEditorId = null;
        let injectionState = false;
        let currentWidth = 300;
        let resizeState = false;
        let currentIndex = 0;

        require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.33.0/min/vs' }});

        require(['vs/editor/editor.main'], function() {
            monaco.editor.defineTheme('incognito', {
                base: 'vs-dark',
                inherit: true,
                rules: [
                    { "token": "keyword", "foreground": "C586C0" },
                    { "token": "constants", "foreground": "4FC1FF" },
                    { "token": "global", "foreground": "569CD6" },
                    { "token": "operator", "foreground": "B0C4DE" },
                    { "token": "variable.language.self", "foreground": "4EC9B0" },
                    { "token": "comment", "foreground": "608B4E" },
                    { "token": "string", "foreground": "CE9178" },
                    { "token": "number", "foreground": "B5CEA8" },
                    { "token": "number.float", "foreground": "B5CEA8" },
                    { "token": "number.hex", "foreground": "B5CEA8" },
                    { "token": "number.binary", "foreground": "B5CEA8" },
                    { "token": "delimiter", "foreground": "569CD6" },
                    { "token": "delimiter.bracket", "foreground": "569CD6" },
                    { "token": "delimiter.array", "foreground": "569CD6" },
                    { "token": "delimiter.parenthesis", "foreground": "569CD6" },
                    { "token": "operator.special", "foreground": "007ACC" },
                    { "token": "variable.parameter.function", "foreground": "9CDCFE" },
                    { "token": "entity.name.function", "foreground": "DCDCAA" },
                    { "token": "support.function", "foreground": "569CD6" },
                    { "token": "support.type", "foreground": "4EC9B0" },
                    { "token": "function.call", "foreground": "DCDCAA" },
                    { "token": "class.name", "foreground": "4EC9B0" },
                    { "token": "type.annotation", "foreground": "569CD6" },
                    { "token": "template.literal", "foreground": "CE9178" },
                    { "token": "modifier", "foreground": "B0C4DE" },
                    { "token": "annotation", "foreground": "FFA500" },
                    { "token": "variable.other.constant", "foreground": "B0C4DE" },
                    { "token": "variable.property", "foreground": "9CDCFE" },
                    { "token": "variable.other.enummember.lua", "foreground": "4EC9B0" },
                    { "token": "support.function.library", "foreground": "569CD6" },
                    { "token": "keyword.control.export", "foreground": "C586C0" },
                    { "token": "storage.type", "foreground": "C586C0" },
                    { "token": "entity.name.type.alias", "foreground": "4EC9B0" },
                    { "token": "punctuation.definition.typeparameters", "foreground": "569CD6" },
                    { "token": "punctuation.definition.block", "foreground": "569CD6" },
                    { "token": "punctuation.separator.table", "foreground": "569CD6" },
                    { "token": "punctuation.definition.parameters", "foreground": "569CD6" },
                    { "token": "variable.parameter.variadic", "foreground": "B0C4DE" },
                    { "token": "keyword.operator.type.annotation", "foreground": "B0C4DE" },
                    { "token": "operator.type", "foreground": "FF0000" },
                    { "token": "punctuation", "foreground": "569CD6" },
                    { "token": "error", "foreground": "FF0000" },
                    { "token": "", "foreground": "B0C4DE" }
                ],
                colors: {
                    'editor.background': '#292929',
                }
            });
            monaco.languages.register({
                id: 'lua',
                extensions: ['.lua'],
                aliases: ['Lua', 'lua'],
            });

            monaco.languages.registerCompletionItemProvider('lua', {
                provideCompletionItems: function(model, position) {
                    const word = model.getWordUntilPosition(position);
                    const range = {
                        startLineNumber: position.lineNumber,
                        endLineNumber: position.lineNumber,
                        startColumn: word.startColumn,
                        endColumn: word.endColumn
                    };

                    const suggestions = [
                        {
                            label: 'function',
                            kind: monaco.languages.CompletionItemKind.Function,
                            insertText: 'function ${1:name}()\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'do',
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: 'do\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'local function',
                            kind: monaco.languages.CompletionItemKind.Function,
                            insertText: 'local function ${1:name}()\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'if',
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: 'if ${1:condition} then\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'while',
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: 'while ${1:condition} do\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'repeat',
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: 'repeat\n\t$0\nuntil ${1:condition}',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'for',
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: 'for ${1:var} = ${2:start}, ${3:end}, ${4:step} do\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        },
                        {
                            label: 'for in',
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: 'for ${1:key}, ${2:value} in pairs(${3:table}) do\n\t$0\nend',
                            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                            range: range
                        }
                    ];

                    const lineTextUntilPosition = model.getValueInRange({
                        startLineNumber: position.lineNumber,
                        startColumn: 1,
                        endLineNumber: position.lineNumber,
                        endColumn: position.column
                    });

                    const match = lineTextUntilPosition.match(/(\w+)\.(\w*)$/);
                    if (match) {
                        const className = match[1];
                        const memberPrefix = match[2].toLowerCase();
                        const members = autocompleteData[className] || [];

                        members.filter(member => memberPrefix === "" || member.toLowerCase().startsWith(memberPrefix))
                            .forEach(member => {
                                suggestions.push({
                                    label: member,
                                    kind: monaco.languages.CompletionItemKind.Method,
                                    insertText: member,
                                    range: range
                                });
                            });
                    } else {
                        const classPrefix = word.word.toLowerCase();
                        Object.keys(autocompleteData).filter(name => name.toLowerCase().startsWith(classPrefix))
                            .forEach(name => {
                                suggestions.push({
                                    label: name,
                                    kind: monaco.languages.CompletionItemKind.Class,
                                    insertText: name,
                                    range: range
                                });
                            });
                    }

                    return { suggestions: suggestions };
                }
            });
            monaco.languages.setMonarchTokensProvider('lua', {
                keywords: 'and break continue do else elseif end for function if in local not or repeat return then until while next'.split(' '),
                constants: 'true false nil'.split(' '),
                brackets: [
                    { token: 'delimiter.bracket', open: '{', close: '}' },
                    { token: 'delimiter.array', open: '[', close: ']' },
                    { token: 'delimiter.parenthesis', open: '(', close: ')' },
                ],
                globals: [
                    'print', 'error', 'warn', 'require', 'game', 'assert',

                    'rawset', 'rawget', 'rawequal',

                    'getupvalue', 'debug.getupvalue',
                    'getconstant', 'debug.getconstant',
                    'setstack', 'debug.setstack',
                    'getproto', 'debug.getproto',
                    'getstack', 'debug.getstack',
                    'getfunctionname', 'debug.getfunctionname',
                    'profilebegin', 'debug.profilebegin',
                    'getprotos', 'debug.getprotos',
                    'traceback', 'debug.traceback',
                    'getconstants', 'debug.getconstants',
                    'getinfo', 'debug.getinfo',
                    'setupvalue', 'debug.setupvalue',
                    'setconstant', 'debug.setconstant',
                    'profileend', 'debug.profileend',
                    'getupvalues', 'debug.getupvalues',

                    'table',
                    'pack', 'table.pack',
                    'move', 'table.move',
                    'insert', 'table.insert',
                    'getn', 'table.getn',
                    'foreachi', 'table.foreachi',
                    'maxn', 'table.maxn',
                    'foreach', 'table.foreach',
                    'concat', 'table.concat',
                    'unpack', 'table.unpack',
                    'find', 'table.find',
                    'create', 'table.create',
                    'sort', 'table.sort',
                    'remove', 'table.remove',

                    'bit32',
                    'bit32.band',
                    'bit32.extract',
                    'bit32.bor',
                    'bit32.bnot',
                    'bit32.arshift',
                    'bit32.rshift',
                    'bit32.rrotate',
                    'bit32.replace',
                    'bit32.lshift',
                    'bit32.lrotate',
                    'bit32.btest',
                    'bit32.bxor',

                    'math',
                    'math.log',
                    'math.ldexp',
                    'math.rad',
                    'math.cosh',
                    'math.random',
                    'math.frexp',
                    'math.tanh',
                    'math.floor',
                    'math.max',
                    'math.sqrt',
                    'math.modf',
                    'math.huge',
                    'math.pow',
                    'math.atan',
                    'math.tan',
                    'math.cos',
                    'math.sign',
                    'math.clamp',
                    'math.log10',
                    'math.noise',
                    'math.acos',
                    'math.abs',
                    'math.pi',
                    'math.sinh',
                    'math.asin',
                    'math.min',
                    'math.deg',
                    'math.fmod',
                    'math.randomseed',
                    'math.atan2',
                    'math.ceil',
                    'math.sin',
                    'math.exp',

                    'string',
                    'string.sub',
                    'string.split',
                    'string.upper',
                    'string.len',
                    'string.find',
                    'string.match',
                    'string.char',
                    'string.rep',
                    'string.gmatch',
                    'string.reverse',
                    'string.byte',
                    'string.format',
                    'string.gsub',
                    'string.lower',

                ],
                operators: [
                    '+', '-', '*', '/', '%', '^', '#', '=',
                    //';', ':', ',', '.', '..', '...', '+=', '-=', '*=', '/=', '..='
                    '..', '...', '+=', '-=', '*=', '/=', '..='
                ],
                special_operators: [
                    '==', '~=', '<=', '>=', '<', '>', '->'
                ],

                symbols: /[=><!~?:&|+\-*\/\^%\#\.]+/,
                escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,
                tokenizer: {
                    root: [
                        [/(?=(function)(\s+[a-zA-Z_][a-zA-Z0-9_]*[\.:][a-zA-Z_][a-zA-Z0-9_]*)(\<.+\>)(\())/, '', '@function_decl'],
                        [/(?=(function)(\s+[a-zA-Z_][a-zA-Z0-9_]*[\.:][a-zA-Z_][a-zA-Z0-9_]*\s*)(\())/, '', '@function_decl'],
                        [/(?=(function)(\s+[a-zA-Z_][a-zA-Z0-9_]*)(\<.+\>)(\())/, '', '@function_decl'],
                        [/(?=(function)(\s+[a-zA-Z_][a-zA-Z0-9_]*\s*)(\())/, '', '@function_decl'],
                        [/(?=(function)(\s+[a-zA-Z_][a-zA-Z0-9_]*\s*)(\())/, '', '@function_decl'],
                        [/(?=(function)(\())/, '', '@function_decl'],

                        [/(?<![^.]\.|:)\b(self)\b/, 'variable.language.self'],
                        [/(?<![^.]\.|:)\b(workspace|game|script|plugin|shared|_G|_VERSION|math\.(pi|huge))\b|(?<![.])\.{3}(?!\.)/, 'constant.language'],
                        [/(?<![^.]\.|:)\b(assert|collectgarbage|error|getfenv|getmetatable|ipairs|loadstring|next|pairs|pcall|print|rawequal|rawget|rawset|require|select|setfenv|setmetatable|tonumber|tostring|type|unpack|xpcall|typeof|wait|delay|settings|elapsedTime|tick|time|warn|spawn|newproxy|UserSettings)\b(?=\s*(?:[({\"']|\[\[))/, 'support.function'],
                        [/(?<![^.]\.|:)\b(coroutine\.(create|resume|running|status|wrap|yield|isyieldable)|string\.(byte|char|dump|find|format|gmatch|gsub|len|lower|match|rep|reverse|sub|upper|split|packsize|pack|unpack)|table\.(concat|insert|maxn|remove|sort|create|find|foreach|foreachi|getn|move|pack|unpack|clear)|math\.(abs|acos|asin|atan2?|ceil|cosh?|deg|exp|floor|fmod|frexp|ldexp|log|log10|max|min|modf|pow|rad|random|randomseed|tointeger|type|ult|noise|clamp|sign|sinh?|sqrt|tanh?|round)|io\.(close|flush|input|lines|open|output|popen|read|tmpfile|type|write)|os\.(clock|date|difftime|execute|exit|getenv|remove|rename|setlocale|time|tmpname)|package\.(cpath|loaded|loadlib|path|preload|seeall)|debug\.(debug|[gs]etfenv|[gs]ethook|getinfo|[gs]etlocal|[gs]etmetatable|getregistry|[gs]etupvalue|traceback|profileend|profilebegin)|utf8\.(char|codes|codepoint|len|offset|graphemes|charpattern|nfcnormalize|nfdnormalize)|bit32\.(arshift|band|bnot|bor|btest|bxor|extract|lrotate|lshift|replace|rrotate|rshift))\b(?=\s*(?:[({\"']|\[\[))/, 'support.function.library'],
                        [/\b(Axes|BrickColor|CFrame|Color3|ColorSequence|ColorSequenceKeypoint|DateTime|DockWidgetPluginGuiInfo|Faces|Instance|NumberRange|NumberSequence|NumberSequenceKeypoint|PathWaypoint|PhysicalProperties|Random|Ray|RaycastParams|Rect|Region3|Region3int16|TweenInfo|UDim|UDim2|Vector2|Vector2int16|Vector3|Vector3int16|Drawing|PD|task)\b/, 'support.type'],
                        [/\b(local)\b/, 'keyword.local'],
                        [/\b(and|break|continue|do|else|elseif|end|for|function|if|in|local|not|or|repeat|return|then|until|while|next)\b/, 'keyword'],

                        [/\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\s*(?:[({\"']|\[\[))/, 'entity.name.function'],
                        [/\b([A-Z_][A-Z0-9_]*)\b/, 'variable.other.constant'],

                        [/(Enum)(\.)(\w*)(\.)(\w*)/, ['variable.other.enummember.lua', '', 'variable.other.enummember.lua', '', 'variable.other.enummember.lua']],
                        [/(Enum)(\.)(\w*)/, ['variable.other.enummember.lua', '', 'variable.other.enummember.lua']],

                        //[/(\bexport\b\s+)(?=(\btype\b\s+)([\w_]+)(<.+>)?(\s*=))/, 'keyword.control.export'],
                        //[/(\btype\b\s+)([\w_]+)(<.+>)(\s*=)/, ['storage.type', 'support.type.alias', '', '']],
                        //[/(\btype\b\s+)([\w_]+)(\s*=)/, ['storage.type', 'support.type.alias', '']],
                        [/(?=\b(export|type)\b\s*[a-zA-Z_])/, '', '@type_decl'],

                        [/[a-zA-Z_]\w*/, {
                            cases: {
                                '@keywords': { token: 'keyword.$0' },
                                '@constants': { token: 'constants.$0' },
                                '@globals': { token: 'global' },
                                '@default': 'identifier'
                            }
                        }],

                        { include: '@whitespace' },

                        [/(?=(\.+[a-zA-Z_][a-zA-Z0-9_]*))(?!(\.+[a-zA-Z_][a-zA-Z0-9_]*)\()/, '', '@index'],

                        //[/(,)(\s*)([a-zA-Z_]\w*)(\s*)(:)(?!:)/, ['delimiter', '', 'key', '', 'delimiter']],
                        //[/({)(\s*)([a-zA-Z_]\w*)(\s*)(:)(?!:)/, ['@brackets', '', 'key', '', 'delimiter']],

                        [/\[([=]*)\[/, 'delimiter.longstring', '@longstring.$1'],
                        [/[{}()\[\]]/, '@brackets'],
                        //[/\.\./, 'operator'],
                        [/@symbols/, {
                            cases: {
                                '@operators': 'operator',
                                '@special_operators': 'operator.special',
                                '@default': ''
                            }
                        }],
                        [/\d*\.\d+([eE][\-+]?\d+)?/, 'number.float'],
                        [/0[xX][0-9a-fA-F_]*[0-9a-fA-F]/, 'number.hex'],
                        [/0[bB][0-9a-fA-F_]*[0-9a-fA-F]/, 'number.binary'],
                        [/\d+?/, 'number'],

                        [/[;,.]/, 'delimiter'],

                        [/"([^"\\]|\\.)*$/, 'string.invalid'],
                        [/'([^'\\]|\\.)*$/, 'string.invalid'],
                        [/"/, 'string.delimeter', '@string."'],
                        [/'/, 'string.delimeter', '@string.\''],
                    ],


                    index: [
                        [/\.[^a-zA-Z_]/, '', '@pop'],
                        [/[a-zA-Z_][a-zA-Z0-9_]*/, 'variable.property', '@pop'],
                    ],

                    type_decl: [
                        [/\s*export\s+/, 'keyword.control.export'],
                        [/\s*type\s+/, 'storage.type'],
                        [/\b[a-zA-Z_][a-zA-Z0-9_]*\b\s*/, 'entity.name.type.alias'],
                        [/\</, 'punctuation.definition.typeparameters', '@type_group'],
                        [/\s*=\s*{/, '@rematch', '@table_type_elements_popall'],
                        [/./, '', '@pop'],
                    ],
                    table_type_elements_popall: [
                        [/(\s*=\s*)({)/, ['keyword.operator', 'punctuation.definition.block']],

                        [/"([^"\\]|\\.)*$/, 'string.invalid'],
                        [/'([^'\\]|\\.)*$/, 'string.invalid'],
                        [/"/, 'string.delimeter', '@string."'],
                        [/'/, 'string.delimeter', '@string.\''],

                        [/[\[\]]/, 'punctuation.definition.block'],
                        [/[a-zA-Z_][a-zA-Z0-9_]*/, 'variable.object.property'],
                        [/{/, 'punctuation.definition.block', '@table_type_elements'],

                        [/: |\?: /, 'keyword.operator.typedef.annotation', '@type_name'],
                        [/[,\;]/, 'punctuation.separator.table'],

                        [/}/, 'punctuation.definition.block', '@popall'],
                        { include: '@whitespace' },
                    ],
                    table_type_elements: [
                        [/"([^"\\]|\\.)*$/, 'string.invalid'],
                        [/'([^'\\]|\\.)*$/, 'string.invalid'],
                        [/"/, 'string.delimeter', '@string."'],
                        [/'/, 'string.delimeter', '@string.\''],

                        [/[\[\]]/, 'punctuation.definition.block'],
                        [/[a-zA-Z_][a-zA-Z0-9_]*/, 'variable.object.property'],
                        [/[\<\>]/, 'punctuation.definition.typeparameters'],
                        [/{/, 'punctuation.definition.block', '@table_type_elements'],

                        [/: |\?: /, 'keyword.operator.typedef.annotation', '@type_name'],
                        [/[,\;]/, 'punctuation.separator.table'],

                        [/}/, 'punctuation.definition.block', '@pop'],
                        { include: '@whitespace' },
                    ],


                    function_decl: [
                        [/function/, 'keyword.control'],
                        [/(\s+[a-zA-Z_][a-zA-Z0-9_]*)([\.:])([a-zA-Z_][a-zA-Z0-9_]*\s*)/, ['entity.name.function', 'punctuation.separator.parameter', 'entity.name.function']],
                        [/\s+[a-zA-Z_][a-zA-Z0-9_]*\s*/, 'entity.name.function'],
                        [/\</, 'punctuation.definition.typeparameters', '@type_group'],
                        [/\(/, 'punctuation.definition.parameters', '@function_params'],
                        [/\)/, 'punctuation.definition.parameters', '@pop'],
                    ],
                    type_operators: [
                        [/(\~|\-\>)/, 'operator.type'],
                        [/[&|?]/, 'punctuation.definition.parameters'],
                        [/\.\.\./, 'variable.parameter.variadic'],
                    ],
                    type_group: [
                        [/[([]/, 'punctuation.definition.parameters', '@type_group'],
                        [/[{]/, 'punctuation.definition.block', '@table_type_elements'], // { exclusive for type tables
                        [/[\<]/, 'punctuation.definition.typeparameters', '@type_group'],
                        [/[a-zA-Z_][a-zA-Z0-9_]*/, 'support.type'],
                        //[/\.\.\./, 'variable.parameter.variadic'],
                        //[/[&|?]/, 'punctuation.definition.parameters'],
                        { include: '@type_operators' },
                        [/,/, 'punctuation'],
                        [/[>]/, 'punctuation.definition.typeparameters', '@pop'],
                        [/[)\]}]/, 'punctuation.definition.parameters', '@pop'],
                    ],
                    type_name: [
                        [/\[,/, 'punctuation.definition.parameters', '@pop'],
                        [/(\(|\[[^\,])/, 'punctuation.definition.parameters', '@type_group'],
                        //[/[\<]/, 'punctuation.definition.typeparameters', '@type_group'],
                        [/[{]/, 'punctuation.definition.block', '@table_type_elements'], // { exclusive for type tables
                        [/[a-zA-Z_][a-zA-Z0-9_]*/, 'support.type'],
                        //[/\.\.\./, 'variable.parameter.variadic'],
                        //[/[&|?]/, 'punctuation.definition.parameters'],
                        [/[\<\>]/, 'punctuation.definition.typeparameters'],
                        //[/->/, 'operator.returns'],
                        //[/[>]/, 'punctuation.definition.typeparameters', '@pop'],
                        { include: '@type_operators' },
                        [/(?=[)\]},;])/, 'punctuation.definition.parameters', '@pop'],
                    ],
                    function_params: [
                        [/[([\]]/, 'punctuation.definition.parameters'],
                        [/\.\.\./, 'variable.parameter.variadic'],
                        [/[a-zA-Z_][a-zA-Z0-9_]*/, 'variable.parameter.function'],
                        [/: |\?: /, 'keyword.operator.type.annotation', '@type_name'],
                        [/,/, 'punctuation.separator.arguments'],
                        [/(?=\))/, '', '@pop'],
                    ],

                    whitespace: [
                        [/[ \t\r\n]+/, ''],
                        [/--\[([=]*)\[/, 'comment', '@comment.$1'],
                        [/--.*$/, 'comment'],
                    ],
                    comment: [
                        [/(?=(\@\w+)((\[\w+\])?\s*)[\{])/, '', '@comment_highlight'],
                        [/(\@)(\w+\s*)/, ['operator', 'comment.highlight.descriptor']],
                        [/\t+\# \w.+/, 'comment.highlight.title'],
                        [/\]([=]*)\]/, {
                            cases: {
                                '$1==$S2': { token: 'comment', next: '@pop' },
                                '@default': 'comment'
                            }
                        }],
                        [/./, 'comment'],
                    ],
                    comment_highlight: [
                        [/(\@)(\w+\s*)/, ['operator', 'comment.highlight.descriptor']],
                        [/(\[)(\w+)(\]\s*)/, ['comment.delimiter.modifier', 'comment.highlight.modifier', 'comment.delimiter.modifier']],
                        [/\{/, 'punctuation.definition.parameters', '@type_group'],
                        [/(([^\t]| )[a-z][a-zA-Z0-9_]*)/, 'comment.highlight.name', '@pop'],
                        [/./, '@rematch', '@pop'],
                    ],
                    longstring: [
                        [/[^\]]+/, 'longstring'],
                        [/\]([=]*)\]/, {
                            cases: {
                                '$1==$S2': { token: 'delimiter.longstring', next: '@pop' },
                                '@default': 'delimiter.longstring'
                            }
                        }],
                        [/./, 'longstring']
                    ],
                    string: [
                        [/[^\\"']+/, 'string'],
                        [/@escapes/, 'string.escape'],
                        [/\\./, 'string.escape.invalid'],
                        [/["']/, {
                            cases: {
                                '$#==$S2': { token: 'string.delimeter', next: '@pop' },
                                '@default': 'string'
                            }
                        }]
                    ],
                }
            });

            monaco.languages.setLanguageConfiguration('lua', {
                comments: {
                    lineComment: '--',
                    blockComment: ['--[[', ']]']
                },
                brackets: [
                    ['{', '}'],
                    ['[', ']'],
                    ['(', ')']
                ],
                autoClosingPairs: [
                    { open: '(', close: ')' },
                    { open: '[', close: ']' },
                    { open: '{', close: '}' },
                    { open: '"', close: '"', notIn: ['string'] },
                    { open: "'", close: "'", notIn: ['string'] },
                    { open: 'function', close: 'end' },
                    { open: 'do', close: 'end' },
                    { open: 'if', close: 'end' },
                    { open: 'repeat', close: 'until' }
                ],
                surroundingPairs: [
                    { open: '{', close: '}' },
                    { open: '[', close: ']' },
                    { open: '(', close: ')' },
                    { open: '"', close: '"' },
                    { open: '\'', close: '\'' }
                ],
                folding: {
                    markers: {
                        start: new RegExp("^\\s*//\\s*(?:(?:#?region\\b)|(?:<editor-fold\\b))"),
                        end: new RegExp("^\\s*//\\s*(?:(?:#?endregion\\b)|(?:</editor-fold>))")
                    }
                }
            });
            newTabButton.addEventListener('click', () => createTab());
        });


        function createTab(fileName, fileContent) {
            const existingNames = Array.from(document.querySelectorAll('.tab span')).map(span => span.textContent.trim());
            let counter = 1;
            let uniqueName = fileName || `Tab ${counter}`;
            
            while (existingNames.includes(uniqueName)) {
                counter++;
                uniqueName = `Tab ${counter}`;
            }

            const editorId = uniqueName;
            const tab = document.createElement('div');
            tab.setAttribute('data-editor-id', editorId);
            tab.className = 'tab';
            tab.innerHTML = `
                <img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACBklEQVR4nO3dQW7TYBCG4VkBR6Ap52DFghUrjgJ0h7lgQawoR0GlCl69KGokQEAbN87nmfH3nGD85pcdjaUkwszMzKwM4AlwAXwGvrOsEbgEnkcnwDPgK/lsgVfR6CRnjNwr9v52kd22fOz9PbmCbenYwDW53LSMTT4v7vnwfwCvoxqSiduZ+sUmmfg1V6/YJBN/ztYnNsnE3/P1iE0y8e8Z68cmmfj/nLVjk0zcPWvd2CQT989bMzbJxGEz14tNMnH43LVik0xMm71ObJKJ6fPXiE0y8bBryB+bZOLh1/HygBXrcu8gyWdzwtiX89abNlw2w5HXc1fscb5y0wfLZtzFPtXJnrfetKFWJRxaw6FFHFrEoUUcWsShRRxaxKFFHFrEoUUcWsShRRxaxKFFKoUegffH7ItnmHmz31mPnUMPkcQ+dtvQZ5EE8LRz6E0kAZx3Dj1EEsCHzqHHY1+ezjDzKh6GpTm0iEOLOLSIQ4s4tEil0KNq13HM17gOoYcKO40Ooc8q7DQ6hN5U2Gl0CD1U2Gl0CD2qdh1rfxiW5tAiDi3i0CIOLeLQIg4t4tAiDi3i0CIOLeLQIg4t4tAiDr2C0Nl+ev6Uvi0ZusqfKczh05Kh37Eeb5YM/Ri4or8vwKPFQv/2F05XzSOfRwb7k/12dx9r8oC8Bj7ubheLn2QzMzOzmOInJvpSwKWQRsYAAAAASUVORK5CYII=">
                <span>${fileName || `${uniqueName}`}</span>
                <img draggable="false" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB40lEQVR4nO2cS2rDQBBEtYpz8ijnyWLQhfK5RRmBDAaHENszPVXd9UDglal+SK0RGvWyGGOMMcYYY4wxxpgbAJwAvAP4Po7990lFFRTyA3gB8IFbNgCvCzkS+f8IyRdWNf8/QvKEVc1/R0hK2RL5HwhJJVsi/3F3bnicNvNuLpP/WPY8S5shu4PkC2tE2H2N2YMtso080S5+40dJdJjszpJ3PpeA0Cv60ka2kY7t4pq3UXlHB28jZCtljboUu7cRhYzyhYA4W5qCQJipC0yFgSjLEBgKBEGGEGYWiiqSZxaMapJnFI6qkiMFoLrkCBGw5LBH4DbgP7neeN/LoLOvdrsQlL2lkUwse0snmVB2XslEsvNLJpBdR/JE2fUkT5BdV3KgbEsOkG3J11h0AHDrSCH5Qt0WAi/vUkqud2bDj+AlJOc/s8EjOa9s8EnOJ5tYch7ZfjkbgLcbBOANNAF4S1gA3uQYgLftBsCwFw4EGYbCVCCIsnSFsTAQZnoK5oJAnC1dIRDImOazXwhlHTWvQ/2je6l5HcpjJKTmdWzCg1Fk5nU08VE/EvM6modXZRpnliW/xIC+LPklRk5myS8xRDVLfomxwFnyH6uRfen3dRyr0me/EM9vjDHGGGOMMcYYswRyBpias+umnbidAAAAAElFTkSuQmCC" class="close-tab" data-editor-id="${editorId}">
            `;
            tabsContainer.appendChild(tab);

            const editorDiv = document.createElement('div');
            editorDiv.style.width = "100%";
            editorDiv.style.height = "100%";
            editorContainer.appendChild(editorDiv);

            const editor = monaco.editor.create(editorDiv, {
                value: fileContent || `print("incognito w")`,
                language: 'lua',
                theme: 'incognito',
                smoothScrolling: true,
                cursorBlinking: "smooth",
                cursorSmoothCaretAnimation: true,
                minimap: { enabled: true } 
            });
            editors[editorId] = editor;
            editorDiv.style.display = 'none';

            tab.addEventListener('click', () => switchTab(editorId));
            tab.querySelector('.close-tab').addEventListener('click', (e) => {
                e.stopPropagation();
                deleteTab(editorId, tab);
            });

            switchTab(editorId);
            tab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
        }

        function switchTab(editorId) {
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => {
                if (tab.getAttribute('data-editor-id') === editorId) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });

            Object.keys(editors).forEach(id => {
                const editorInstance = editors[id];
                const editorDomNode = editorInstance.getContainerDomNode();
                if (editorDomNode) {
                    editorDomNode.style.display = 'none';
                }
            });

            const activeEditor = editors[editorId];
            if (activeEditor) {
                const activeEditorDomNode = activeEditor.getContainerDomNode();
                if (activeEditorDomNode) {
                    activeEditorDomNode.style.display = 'block';
                    activeEditor.layout();
                }
                activeEditorId = editorId;
            } else {
                console.log(`Editor ID ${editorId} does not exist.`);
            }
        }

        function deleteTab(editorId, tab) {
            editors[editorId].dispose();

            const editorContainerDiv = editors[editorId].getContainerDomNode();
            if (editorContainerDiv && editorContainerDiv.parentNode) {
                editorContainerDiv.parentNode.removeChild(editorContainerDiv);
            }
            delete editors[editorId];
            tab.remove();

            if (Object.keys(editors).length === 0) {
                editorContainer.innerHTML = '';
                activeEditorId = null;
            } else {
                switchTab(Object.keys(editors)[0]);
            }
        }

        function toggleWindowResize(arg) {
            resizeState = arg;
        }

        function fetchScripts() {
            pywebview.api.FetchStoredScripts().then(files => {
                const filesArray = JSON.parse(files);
                const container = document.querySelector('.files-container');
                container.innerHTML = '';
                filesArray.forEach(fileObj => {
                    const fileWrapper = document.createElement('div');
                    fileWrapper.className = 'file-wrapper';

                    const fileDiv = document.createElement('div');
                    fileDiv.className = 'file';

                    const img = document.createElement('img');
                    img.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACBklEQVR4nO3dQW7TYBCG4VkBR6Ap52DFghUrjgJ0h7lgQawoR0GlCl69KGokQEAbN87nmfH3nGD85pcdjaUkwszMzKwM4AlwAXwGvrOsEbgEnkcnwDPgK/lsgVfR6CRnjNwr9v52kd22fOz9PbmCbenYwDW53LSMTT4v7vnwfwCvoxqSiduZ+sUmmfg1V6/YJBN/ztYnNsnE3/P1iE0y8e8Z68cmmfj/nLVjk0zcPWvd2CQT989bMzbJxGEz14tNMnH43LVik0xMm71ObJKJ6fPXiE0y8bBryB+bZOLh1/HygBXrcu8gyWdzwtiX89abNlw2w5HXc1fscb5y0wfLZtzFPtXJnrfetKFWJRxaw6FFHFrEoUUcWsShRRxaxKFFHFrEoUUcWsShRRxaxKFFKoUegffH7ItnmHmz31mPnUMPkcQ+dtvQZ5EE8LRz6E0kAZx3Dj1EEsCHzqHHY1+ezjDzKh6GpTm0iEOLOLSIQ4s4tEil0KNq13HM17gOoYcKO40Ooc8q7DQ6hN5U2Gl0CD1U2Gl0CD2qdh1rfxiW5tAiDi3i0CIOLeLQIg4t4tAiDi3i0CIOLeLQIg4t4tAiDr2C0Nl+ev6Uvi0ZusqfKczh05Kh37Eeb5YM/Ri4or8vwKPFQv/2F05XzSOfRwb7k/12dx9r8oC8Bj7ubheLn2QzMzOzmOInJvpSwKWQRsYAAAAASUVORK5CYII=';

                    fileDiv.appendChild(img);

                    const textNode = document.createTextNode(fileObj.name);
                    fileDiv.appendChild(textNode);

                    fileWrapper.appendChild(fileDiv);
                    container.appendChild(fileWrapper);

                    fileDiv.addEventListener('click', () => {
                        let fileName = fileObj.name;
                        fileName = fileName.replace(/\.lua$/, '');

                        if (!editors.hasOwnProperty(fileName)) {
                            createTab(fileName, fileObj.content);
                        } else {
                            switchTab(fileName);
                        }
                    });
                });
            });
        }

        function updateUnderline(activeDiv) {
            underline.style.width = `${activeDiv.clientWidth}px`;
            underline.style.left = `${activeDiv.offsetLeft}px`;
        }

        const firstIcon = topIsland[0];
        updateUnderline(firstIcon);

        topIsland.forEach((div, index) => {
            div.addEventListener('click', function() {
                currentIndex = index;
                updateUnderline(this);

                setTimeout(() => {
                    underline.style.width = `${this.clientWidth}px`;
                }, 150);

                if (index === 0) {
                    mainBackground.style.display = 'flex';
                    settingsBackground.style.display = 'none';
                } else if (index === 1) {
                    mainBackground.style.display = 'none';
                    settingsBackground.style.display = 'flex';
                }
            });
        });

        window.addEventListener('pywebviewready', function () {
            pywebview.api.FetchAppVersion().then((version) => {
                versionLabel.innerHTML = `v${version}`
            })

            fetchScripts();
            
            pywebview.api.FetchIDEData().then((data) => {
                const apiData = JSON.parse(data);

                Object.keys(apiData).forEach(key => {
                    const match = key.match(/@roblox\/(globaltype|global)\/([^\.]+)/);
                    if (match) {
                        const type = match[1];
                        const className = match[2];
                        if (!autocompleteData[className]) {
                            autocompleteData[className] = [];
                        }
                        if (type === 'global') {

                            const members = apiData[key].keys || {};
                            autocompleteData[className].push(...Object.keys(members));
                        }
                    }
                });
            });

            
            setInterval(() => {
                const tabsData = [];
                document.querySelectorAll('.tab').forEach(tab => {
                    const editorId = tab.getAttribute('data-editor-id');
                    const editor = editors[editorId];
                    const content = editor.getValue();
                    const tabName = tab.querySelector('span').textContent;
                    tabsData.push({ name: tabName, content: content });
                });

                pywebview.api.SaveTabs(JSON.stringify(tabsData));
            }, 5000);

            pywebview.api.LoadTabs().then((tabsJson) => {
                const response = JSON.parse(tabsJson);
                const tabs = response.tabs;

                if (response.count > 0) {
                    tabs.forEach(tab => {
                        createTab(tab.name, tab.content);
                    });
                } else {
                    console.log('No saved tabs to load');
                    createTab('Tab 1', 'print("incognito w")')
                }
            }).catch(error => {
                console.log('Error loading tabs:', error);
            });
            
        });


        document.addEventListener('DOMContentLoaded', function() {
            const clearButton = document.getElementById('clear');
            clearButton.addEventListener('click', function() {
                if (activeEditorId !== null && editors.hasOwnProperty(activeEditorId)) {
                    const activeEditor = editors[activeEditorId];
                    console.log(activeEditor)
                    activeEditor.setValue('');
                }
            });

            if (attachButton) {
                attachButton.addEventListener('click', function() {
                    if (injectionState) {
                        showNotification("Already Injected!", "Incognito");
                        return;
                    }

                    if (statusDiv) {
                        statusDiv.classList.add('loading');
                    }

                    pywebview.api.InitInject().then(response => {
                        const result = JSON.parse(response);

                        setTimeout(() => {
                            if (result.message == "Successfully injected!") {
                                if (statusDiv) {
                                    statusDiv.style.backgroundColor = '#88ff00';
                                    statusDiv.classList.remove('loading');
                                }
                                injectionState = true;
                            } else {
                                if (statusDiv) {
                                    statusDiv.style.backgroundColor = 'red';
                                    statusDiv.classList.remove('loading');
                                }
                            }
                            showNotification(result.message, "Incognito");
                        }, 1500);

                    }).catch(error => {
                        setTimeout(() => {
                            showNotification("Failed to inject due to an error.", "Incognito");
                            if (statusDiv) {
                                statusDiv.style.backgroundColor = 'red';
                                statusDiv.classList.remove('loading');
                            }
                        }, 1500);
                    });
                });
            }
                    
            if (executeButton) {
                executeButton.addEventListener('click', function() {
                    const activeEditor = editors[activeEditorId];
                    pywebview.api.ExecuteScript(activeEditor.getValue())
                });
            }

            if (newFile) {
                newFile.addEventListener('click', function() {
                    const container = document.querySelector('.files-container');
                    const fileWrapper = document.createElement('div');
                    fileWrapper.className = 'file-wrapper';

                    const fileDiv = document.createElement('div');
                    fileDiv.className = 'file';

                    const img = document.createElement('img');
                    img.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACBklEQVR4nO3dQW7TYBCG4VkBR6Ap52DFghUrjgJ0h7lgQawoR0GlCl69KGokQEAbN87nmfH3nGD85pcdjaUkwszMzKwM4AlwAXwGvrOsEbgEnkcnwDPgK/lsgVfR6CRnjNwr9v52kd22fOz9PbmCbenYwDW53LSMTT4v7vnwfwCvoxqSiduZ+sUmmfg1V6/YJBN/ztYnNsnE3/P1iE0y8e8Z68cmmfj/nLVjk0zcPWvd2CQT989bMzbJxGEz14tNMnH43LVik0xMm71ObJKJ6fPXiE0y8bBryB+bZOLh1/HygBXrcu8gyWdzwtiX89abNlw2w5HXc1fscb5y0wfLZtzFPtXJnrfetKFWJRxaw6FFHFrEoUUcWsShRRxaxKFFHFrEoUUcWsShRRxaxKFFKoUegffH7ItnmHmz31mPnUMPkcQ+dtvQZ5EE8LRz6E0kAZx3Dj1EEsCHzqHHY1+ezjDzKh6GpTm0iEOLOLSIQ4s4tEil0KNq13HM17gOoYcKO40Ooc8q7DQ6hN5U2Gl0CD1U2Gl0CD2qdh1rfxiW5tAiDi3i0CIOLeLQIg4t4tAiDi3i0CIOLeLQIg4t4tAiDr2C0Nl+ev6Uvi0ZusqfKczh05Kh37Eeb5YM/Ri4or8vwKPFQv/2F05XzSOfRwb7k/12dx9r8oC8Bj7ubheLn2QzMzOzmOInJvpSwKWQRsYAAAAASUVORK5CYII=';
                    fileDiv.appendChild(img);

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.placeholder = '';
                    input.className = 'file-name-input';
                    fileDiv.appendChild(input);
                    input.focus()

                    fileWrapper.appendChild(fileDiv);
                    container.appendChild(fileWrapper);

                    function finalizeFile(fileName) {
                        const ffName = fileName + '.lua';
                        if (!editors.hasOwnProperty(ffName)) {
                            createTab(ffName);
                        } else {
                            switchTab(ffName);
                        }
                        pywebview.api.CreateScriptFile(ffName)
                        input.replaceWith(document.createTextNode(ffName));

                    }

                    input.addEventListener('blur', function() {
                        const fileName = input.value.trim();
                        if (fileName) {
                            finalizeFile(fileName);
                        } else {
                            fileWrapper.remove();
                        }
                    });

                    input.addEventListener('keypress', function(event) {
                        if (event.key === 'Enter') {
                            const fileName = input.value.trim();
                            if (fileName) {
                                finalizeFile(fileName);
                            } else {
                                fileWrapper.remove();
                            }
                        }
                    });
                });
            }
        });

        if (saveFile) {
            saveFile.addEventListener('click', function() {
                if (activeEditorId !== null && editors.hasOwnProperty(activeEditorId)) {
                    const activeEditor = editors[activeEditorId];
                    const content = activeEditor.getValue();
                    const fileName = activeEditorId;

                    pywebview.api.SaveScriptFile(fileName, content)
                        .then(() => {
                            console.log('File saved successfully');
                        })
                        .catch(error => {
                            console.error('Error saving file:', error);
                        });
                } else {
                    console.log('No active editor to save');
                }
                setTimeout(() => {
                    fetchScripts();
                }, 2000);
            });
        }

        if (saveAll) {
            saveAll.addEventListener('click', function() {
                const filesToSave = [];
                Object.keys(editors).forEach(editorId => {
                    const editor = editors[editorId];
                    const content = editor.getValue();
                    filesToSave.push({ fileName: editorId, content: content });
                });

                pywebview.api.SaveAllScripts(filesToSave)
                    .then(() => {
                        console.log('All files saved successfully');
                    })
                    .catch(error => {
                        console.error('Error saving files:', error);
                    });

                setTimeout(() => {
                    fetchScripts();
                }, 2000);
            });
        }

        if (undoButton) {
            undoButton.addEventListener('click', function() {
                if (activeEditorId !== null && editors.hasOwnProperty(activeEditorId)) {
                    const activeEditor = editors[activeEditorId];
                    activeEditor.trigger('keyboard', 'undo', null);
                } else {
                    console.log('No active editor to undo');
                }
            });
        }

        if (redoButton) {
            redoButton.addEventListener('click', function() {
                if (activeEditorId !== null && editors.hasOwnProperty(activeEditorId)) {
                    const activeEditor = editors[activeEditorId];
                    activeEditor.trigger('keyboard', 'redo', null);
                } else {
                    console.log('No active editor to redo');
                }
            });
        }

        if (minimize) {
            minimize.addEventListener('click', function() {
                pywebview.api.MinimizeWindow()
            });
        }

        if (closeButton) {
            closeButton.addEventListener('click', function() {
                pywebview.api.CloseWindow()
            });
        }

        if (consoleButton) {
            consoleButton.addEventListener('click', function() {
                pywebview.api.ConsoleWindow().then(() => {
                    if (consoleButton.style.border === '1px solid white') {
                        consoleButton.style.border = 'none';
                    } else {
                        consoleButton.style.border = '1px solid white';
                    }
                });
            });
        }

        folderArrow.addEventListener('click', function() {
            if (filesContainer.classList.contains('collapsed')) {
                filesContainer.classList.remove('collapsed');
                folderArrow.classList.remove('rotated');

                filesContainer.style.maxHeight = '250px';
            } else {
                filesContainer.classList.add('collapsed');
                folderArrow.classList.add('rotated');
                filesContainer.style.maxHeight = null;
            }
        });

        function showNotification(message, title) {
            if (message.includes('detached!')) {
                injectionState = false;
            }

            const notification = document.createElement('div');
            notification.className = 'notification';

            const titleElement = document.createElement('div');
            titleElement.className = 'notification-title';
            titleElement.textContent = title || 'Incognito';

            const messageElement = document.createElement('div');
            messageElement.className = 'notification-message';
            messageElement.textContent = message;

            notification.appendChild(titleElement);
            notification.appendChild(messageElement);
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.classList.add('show');
            }, 10);

            setTimeout(() => {
                notification.classList.add('hide');
                setTimeout(() => {
                    notification.classList.remove('show');
                    notification.style.animation = 'hideNotification 0.8s forwards';
                    setTimeout(() => document.body.removeChild(notification), 800);
                }, 300);
            }, 3000);
        }

        function handleCategoryInteract() {
            if (this instanceof Element) { 
                const cIndex = Array.from(settingCategories).indexOf(this);
                const cHeader = settingHeaders[cIndex];

                if (cHeader) {
                    const hTop = cHeader.getBoundingClientRect().top;
                    const cTop = settingsContainer.getBoundingClientRect().top;
                    const sTarget = settingsContainer.scrollTop + hTop - cTop - 10;

                    settingsContainer.scrollTo({
                        top: sTarget,
                        behavior: 'smooth'
                    });
                }
            }

            let chIndex = -1;
            let minDisTop = Infinity;

            settingHeaders.forEach((header, index) => {
                const rect = header.getBoundingClientRect();
                const topDis = rect.top - settingsContainer.getBoundingClientRect().top;

                if (topDis > 0 && topDis < minDisTop) {
                    minDisTop = topDis;
                    chIndex = index;
                }
            });

            settingCategories.forEach((category, index) => {
                if (index === chIndex) {
                    category.classList.add('active');
                } else {
                    category.classList.remove('active');
                }
            });
        }

        function setAnimDuration(speed) {
            const skipUrls = [
                'https://fonts.googleapis.com/css',
                'https://cdnjs.cloudflare.com'
            ];

            for (let i = 0; i < document.styleSheets.length; i++) {
                const sheet = document.styleSheets[i];

                if (skipUrls.some(url => sheet.href && sheet.href.startsWith(url))) {
                    console.log("Skipping:", sheet.href);
                    continue;
                }

                try {
                    const rules = sheet.cssRules || sheet.rules;
                    for (let j = 0; j < rules.length; j++) {
                        const rule = rules[j];
                        if (rule.type === CSSRule.STYLE_RULE) {
                            const ruleSelector = rule.selectorText;

                            if (rule.style.animationName !== '') {
                                if (!orgDuration[ruleSelector]) {
                                    orgDuration[ruleSelector] = {
                                        animation: rule.style.animationDuration,
                                        transition: rule.style.transitionDuration
                                    };
                                }
                                rule.style.animationDuration = speed === "restore" ? orgDuration[ruleSelector].animation : speed;
                            }

                            if (rule.style.transitionDuration !== '') {
                                if (!orgDuration[ruleSelector]) {
                                    orgDuration[ruleSelector] = {
                                        animation: rule.style.animationDuration,
                                        transition: rule.style.transitionDuration
                                    };
                                }
                                rule.style.transitionDuration = speed === "restore" ? orgDuration[ruleSelector].transition : speed;
                            }
                        }
                    }
                } catch (e) {
                    console.error(sheet.href);
                    continue;
                }
            }
        }

        settingCategories.forEach(category => {
            category.addEventListener('click', handleCategoryInteract);
        });

        settingsContainer.addEventListener('scroll', handleCategoryInteract);
        
        settingsButton.addEventListener('click', function() {
            settingsBackground.style.display = 'block';
            settingsBackground.style.opacity = 1;
        });
        
        // for type 2 buttons
        settingsType2Buttons.forEach(button => {
            button.addEventListener('click', function() {
                const settingOption = button.closest('.setting-option');
                const settingTitle = settingOption.querySelector('.settings-title').textContent.trim();
                const currentState = button.getAttribute('data-enabled') === 'true';

                button.setAttribute('data-enabled', `${!currentState}`);
                button.style.backgroundColor = currentState ? '' : '#B2EC5D'; 

                switch (settingTitle) {
                    // General
                    case 'Top Most':
                        if (currentState) {
                            pywebview.api.topMost("disable")
                        } else {
                            pywebview.api.topMost("enable")
                        }
                        break;
                    case 'Lock Window Size':
                        if (currentState) {
                            toggleWindowResize(false);
                        } else {
                            toggleWindowResize(true);
                        }
                        break;
                    case 'Reduce Animations':
                        if (currentState) {
                            console.log("restoring")
                            setAnimDuration("restore");
                        } else {
                            console.log("removng")
                            setAnimDuration("0.001s");
                        }
                        break;

                        
                    // Layout
                    case 'Lua Language Server':
                        if (currentState) {
                            // disabled
                        } else {
                            // enabled
                        }
                        break;
                    case 'Minimap':
                        Object.keys(editors).forEach(editorId => {
                            const editor = editors[editorId];
                            if (editor) {
                                editor.updateOptions({
                                    minimap: { enabled: !currentState }
                                });
                            }
                        });
                        break;
                    case 'Smooth Cursor':
                        if (currentState) {
                            // disabled
                        } else {
                            // enabled
                        }
                        break;
                    case 'Smooth Scroll':
                        if (currentState) {
                            // disabled
                        } else {
                            // enabled
                        }
                        break;
                    default:
                        console.log('No action for:', settingTitle);
                }
            });
        });

        window.addEventListener('resize', function() {
            const activeDiv = topIsland[currentIndex];
            updateUnderline(activeDiv);

            Object.keys(editors).forEach(function(editorId) {
                if (editors[editorId]) {
                    editors[editorId].layout();
                }
            });
        });

        (function() {
            var initialX = 0;
            var initialY = 0;

            function onMouseMove(ev) {
                var x = ev.screenX - initialX;
                var y = ev.screenY - initialY;
                pywebview._bridge.call('pywebviewMoveWindow', [x, y], 'move');
            }

            function onMouseUp() {
                window.removeEventListener('mousemove', onMouseMove);
                window.removeEventListener('mouseup', onMouseUp);
            }

            function onMouseDown(ev) {
                initialX = ev.clientX;
                initialY = ev.clientY;
                window.addEventListener('mouseup', onMouseUp);
                window.addEventListener('mousemove', onMouseMove);
            }

            dragRegion.addEventListener('mousedown', onMouseDown);
        })();

        handles.forEach(handle => {
            document.getElementById(`${handle}-handle`).addEventListener('mousedown', function(event) {
                console.log(resizeState)
                if (event.which === 1 && !resizeState) { 
                    window.pywebview.api.startResize(handle);
                }
            });
        });

        function initResize(e) {
            currentWidth = parseInt(leftContainer.style.width, 10) || leftContainer.offsetWidth;
            window.addEventListener('mousemove', startResizing, false);
            window.addEventListener('mouseup', stopResizing, false);
        }

        function startResizing(e) {
            const newWidth = e.clientX - leftContainer.getBoundingClientRect().left;
            if (newWidth > 270) {
                leftContainer.style.width = newWidth + 'px';
                currentWidth = newWidth;
                leftContainer.style.overflow = 'visible';
            }  else if (newWidth > 130) {
                leftContainer.style.width = '270px';
                currentWidth = 270;
                leftContainer.style.overflow = 'visible';
                if (infoContainer && fileSystemButtons && folderHeader && fileWrapper) {
                    infoContainer.querySelectorAll('h2, span').forEach(element => {
                        element.style.display = 'flex';
                    });
                    fileSystemButtons.style.display = 'flex';
                    folderHeader.style.display = 'flex';
                    fileWrapper.style.display = 'flex';
                } else {
                    console.log("Visible Error");
                }
            } else if (newWidth < 130) {
                leftContainer.style.width = '94px';
                currentWidth = 94;
                leftContainer.style.overflow = 'hidden';
                if (infoContainer && fileSystemButtons && folderHeader && fileWrapper) {
                    infoContainer.querySelectorAll('h2, span').forEach(element => {
                        element.style.display = 'none';
                    });
                    fileSystemButtons.style.display = 'none';
                    folderHeader.style.display = 'none';
                    fileWrapper.style.display = 'none';
                } else {
                    console.log("None Error");
                }
            }
            Object.keys(editors).forEach(function(editorId) {
                if (editors[editorId]) {
                    editors[editorId].layout();
                }
            });
        }

        function stopResizing(e) {
            window.removeEventListener('mousemove', startResizing, false);
            window.removeEventListener('mouseup', stopResizing, false);
        }

        resizeHandle.addEventListener('mousedown', initResize, false);
    </script>
</body>
</html>


"""
