import React from 'react';
import {
  AbsoluteFill,
  Composition,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const orange = '#DF6F28';
const purple = '#4B3F72';
const ink = '#17130F';
const paper = '#FFFCF6';

const Pulse = ({
  left,
  top,
  delay,
  color,
}: {
  left: string;
  top: string;
  delay: number;
  color: string;
}) => {
  const frame = useCurrentFrame();
  const local = (frame + delay) % 90;
  const scale = interpolate(local, [0, 38, 90], [0.82, 1.14, 0.82]);
  const ring = interpolate(local, [0, 48, 90], [0, 30, 0]);
  const opacity = interpolate(local, [0, 42, 90], [0.85, 0.18, 0.85]);

  return (
    <div
      style={{
        position: 'absolute',
        left,
        top,
        width: 20,
        height: 20,
        borderRadius: '50%',
        background: color,
        transform: `translate(-50%, -50%) scale(${scale})`,
        boxShadow: `0 0 0 ${ring}px ${color}${Math.round(opacity * 255)
          .toString(16)
          .padStart(2, '0')}`,
      }}
    />
  );
};

export const BuyerMapHero = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const progress = frame / durationInFrames;
  const drift = interpolate(frame, [0, durationInFrames], [0, -36]);
  const imageScale = interpolate(frame, [0, durationInFrames], [1.035, 1.07]);
  const lineScale = interpolate(
    Math.sin(progress * Math.PI * 2),
    [-1, 1],
    [0.72, 1.02],
  );

  return (
    <AbsoluteFill
      style={{
        background: paper,
        overflow: 'hidden',
        fontFamily: 'Outfit, Arial, sans-serif',
      }}
    >
      <Img
        src={staticFile('aa-buyer-map-hero-v2.png')}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `translateX(${drift}px) scale(${imageScale})`,
          filter: 'saturate(0.96) contrast(1.03)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(90deg, rgba(255,252,246,.24), rgba(255,252,246,0) 42%), radial-gradient(circle at 74% 54%, rgba(223,111,40,.18), transparent 28%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: '30%',
          top: '56%',
          width: '44%',
          height: 6,
          borderRadius: 999,
          background: `linear-gradient(90deg, transparent, ${orange}, ${purple}, transparent)`,
          opacity: 0.88,
          transform: `rotate(-7deg) scaleX(${lineScale})`,
          transformOrigin: 'left center',
        }}
      />
      <Pulse left="42%" top="59%" delay={0} color={orange} />
      <Pulse left="68%" top="45%" delay={24} color={purple} />
      <Pulse left="80%" top="36%" delay={48} color={orange} />
      <div
        style={{
          position: 'absolute',
          right: 54,
          bottom: 48,
          width: 290,
          padding: '22px 24px',
          borderRadius: 16,
          background: 'rgba(23,19,15,.82)',
          border: '1px solid rgba(255,255,255,.16)',
          color: paper,
          boxShadow: '0 24px 60px rgba(23,19,15,.2)',
        }}
      >
        <div
          style={{
            color: orange,
            fontSize: 15,
            textTransform: 'uppercase',
            letterSpacing: 1.4,
            marginBottom: 8,
          }}
        >
          Outreach path
        </div>
        <div style={{fontSize: 25, lineHeight: 1.16, fontWeight: 700}}>
          From market to decision-maker
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          border: `18px solid rgba(255,252,246,.24)`,
          boxShadow: `inset 0 0 0 1px rgba(23,19,15,.08)`,
        }}
      />
    </AbsoluteFill>
  );
};

export const RemotionRoot = () => (
  <Composition
    id="BuyerMapHero"
    component={BuyerMapHero}
    durationInFrames={180}
    fps={30}
    width={1536}
    height={1024}
  />
);
