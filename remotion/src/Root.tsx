import React from 'react';
import {Composition} from 'remotion';
import {TitleDemo} from './TitleDemo';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="TitleDemo"
    component={TitleDemo}
    durationInFrames={90}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{title: 'AI MASTER', subtitle: 'Remotion OK'}}
  />
);
