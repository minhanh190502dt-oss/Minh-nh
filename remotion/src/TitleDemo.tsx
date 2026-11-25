import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const TitleDemo: React.FC<{title: string; subtitle: string}> = ({title, subtitle}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scale = spring({frame, fps, config: {damping: 12}});
  const opacity = interpolate(frame, [15, 35], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: 'linear-gradient(160deg,#0f172a,#1e3a8a)', justifyContent: 'center', alignItems: 'center', fontFamily: 'sans-serif'}}>
      <div style={{transform: `scale(${scale})`, color: 'white', fontSize: 140, fontWeight: 900}}>{title}</div>
      <div style={{opacity, color: '#facc15', fontSize: 64, marginTop: 30}}>{subtitle}</div>
    </AbsoluteFill>
  );
};
