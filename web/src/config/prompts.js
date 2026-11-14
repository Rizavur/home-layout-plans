// Text for the "AI render" prompts (ChatGPT or any image AI).
// buildPrompt() assembles one prompt from the current scene, theme, furniture, ceiling and lighting.
import { roomOf } from './rooms.js';

export const THEME_TEXT = {
  lux: 'Modern luxury: warm white walls, dark walnut veneer, white Calacatta marble, champagne-brass accents, greige boucle and soft taupe textiles',
  japandi: 'Japandi: warm white walls, natural light oak, slatted timber, black metal details, linen upholstery, muted sage accents, calm and uncluttered',
  nordic: 'Nordic / Scandinavian: bright white walls, pale birch and oak, light grey fabrics, dusty-blue and sage accents, brushed steel, airy and light',
  midcentury: 'Mid-century modern: warm white walls, teak and walnut wood, teal-green upholstery, mustard and burnt-orange cushions, brass details',
  industrial: 'Industrial loft: concrete-grey walls and floor, smoked dark oak, black powder-coated steel, cognac leather, charcoal textiles',
  classic: 'Modern classic: soft ivory and greige walls, oak floor tone, white marble, antique brass, navy and champagne textiles',
  wabisabi: 'Wabi-sabi: clay limewash walls, warm stone floor, weathered grey-brown timber, unbleached linen, charcoal and rust accents, matte and imperfect',
  minimal: 'Minimalist: near-white walls and floor, very pale oak, soft greys, thin black metal accents, almost no colour, very clean',
  coastal: 'Coastal: crisp white walls, sandy light oak, white and sand linen, soft sea-blue and seafoam cushions, natural rattan',
  boho: 'Boho: warm cream walls, honey-toned wood, terracotta, mustard, olive and deep-teal textiles, natural rattan, relaxed and layered',
  deco: 'Art Deco: deep emerald walls, black and white marble, polished brass, emerald velvet with blush and black accents, glamorous',
  dark: 'Dark luxe: mocha walls, black marble, dark walnut, gold accents, oxblood and deep-green cushions, moody and rich',
};

export const FURNITURE_TEXT = {
  lux: 'curved boucle sofa with plush cushions, upholstered channel-tufted headboard, marble-top dining table on sculpted walnut trestle legs, armless cognac leather dining chairs with black legs, pebble-shaped coffee table, brass linear pendant',
  japandi: 'low oak platform sofa with loose linen cushions, low oak platform bed with slatted headboard, solid oak trestle dining table, wishbone chairs with woven cane seats, paper lantern lights',
  scandi: 'sofa raised on slim tapered oak legs, light bed frame on tapered legs, rounded oak dining table on splayed legs, moulded shell dining chairs, oval oak coffee table, white dome pendants, tripod floor lamp',
  midcentury: 'walnut-framed sofa with tufted bench seat and bolsters, wide walnut panel headboard, walnut dining table on tapered splayed legs, curved-back walnut chairs, Eames-style lounge chair, opal globe lights',
  industrial: 'boxy leather sofa in a black steel frame, black steel bar headboard bed, thick timber slab dining table on steel X-frame legs, metal cafe chairs, factory cone pendants',
  classic: 'Chesterfield sofa with rolled arms and button tufting, arched wingback tufted headboard, marble dining table on turned pedestals, upholstered Louis-style chairs, brass lantern pendants',
};

export const CEILING_TEXT = {
  wave: 'white plasterboard false ceiling with an organic free-form recessed cove and hidden warm LED strip lighting',
  crescent: 'white plasterboard false ceiling with a crescent-moon-shaped recessed cove, hidden warm LED glow along its edge and a thin brass inlay line',
  arc: 'white plasterboard false ceiling with a recessed cove whose one long side is a single sweeping curve, hidden warm LED glow and a thin brass inlay line',
  pill: 'white plasterboard false ceiling with a rounded pill-shaped recessed cove and a floating brass-edged inner panel, warm LED halo',
  island: 'white plasterboard false ceiling with a softly rounded tray and a floating pebble-shaped panel inside it, warm LED halo all around',
};

export const LIGHTING = {
  day: ['Daytime', 'bright natural daylight streaming through the windows, soft shadows, lights off except the cove lighting'],
  golden: ['Golden hour', 'late-afternoon golden-hour sun through the windows, warm long shadows, cove lighting softly on'],
  night: ['Evening, lights on', 'evening, dark outside the windows, all interior lights on: warm 3000K cove lighting, downlights and lamps, cosy atmosphere'],
};

/**
 * @param {object} p
 * @param {string} p.viewName   scene name, e.g. "Living – TV wall"
 * @param {boolean} p.fromAbove camera is above the ceiling (plan view)
 * @param {string} p.theme      theme key
 * @param {string} p.family     furniture family key
 * @param {string} p.ceiling    ceiling design key
 * @param {string} p.lighting   'day' | 'golden' | 'night'
 */
export function buildPrompt({ viewName, fromAbove, theme, family, ceiling, lighting }) {
  if (fromAbove) {
    return [
      'Turn this 3D screenshot into a photorealistic top-down 3D floor plan render (cutaway, no ceiling) of a 5-room HDB flat in Singapore.',
      'Keep the exact layout, walls, doors, windows, furniture positions and sizes – do not add, remove or move anything.',
      `Interior style: ${THEME_TEXT[theme]}.`,
      `Furniture: ${FURNITURE_TEXT[family]}.`,
      'Realistic materials and textures, soft daylight from above, gentle ambient occlusion, clean white background. No text, labels or watermarks.',
    ].join('\n');
  }
  const room = roomOf(viewName);
  const detail = viewName.split(' – ')[1] || viewName;
  const where = room.toLowerCase() + (detail && detail !== room ? ` (${detail.toLowerCase()})` : '');
  return [
    'Turn this 3D screenshot into a photorealistic interior photograph. Keep the exact same camera angle, room layout, walls, windows, doors, built-in carpentry, furniture positions, sizes and proportions – do not add, remove or move anything, and keep the ceiling design exactly as shown.',
    '',
    `Room: ${where} in a 5-room HDB flat in Singapore, 2.65 m ceiling with a false ceiling at 2.55 m.`,
    `Style: ${THEME_TEXT[theme]}.`,
    `Furniture: ${FURNITURE_TEXT[family]}.`,
    `Ceiling: ${CEILING_TEXT[ceiling]}.`,
    `Lighting: ${LIGHTING[lighting][1]}.`,
    'Materials: realistic textures – wood grain, natural stone veining, fabric weave, matte painted walls, large-format floor tiles; replace any flat or blocky shapes with their realistic real-world equivalents.',
    '',
    'Photography: architectural interior photo for a design magazine, full-frame camera, 24 mm lens at eye level, vertical lines kept straight, natural colours, realistic soft shadows and global illumination, high detail. No people, no text, no watermarks.',
  ].join('\n');
}
