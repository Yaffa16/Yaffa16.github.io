/* =================================================================
   WEIRD WITH CODE — single source of truth for the works index.
   Paths are relative to the /work/ directory. Pages set
   window.WC_BASE ('work/' from root, '' from inside /work/) before
   loading this file.

   To add a project: drop a new object at the top of the right year.
   Nothing else needs editing — both the homepage and the works page
   read from here.
   ================================================================= */

window.WC_WORKS = [
  { year: 2025, items: [
    { t: 'Animated Drawings',   h: '2025/Animated_Drawings.html',   i: '2025/Animated_Drawings.jpg',   g: 'Generative · Installation', d: 'A generative drawing system that produces evolving animated illustrations in real time, blurring authorship between artist and algorithm.', v: 'Personal project' },
    { t: 'Electronic Petting Zoo', h: '2025/Electronic_Petting_Zoo.html', i: '2025/Electronic_Petting_Zoo.jpg', g: 'Installation', d: 'An interactive installation where visitors interact with electronic pets that respond to touch and sound.', v: 'Commission' },
    { t: 'Bring Your Own Model', h: '2025/Bring_Your_Own_Model.html', i: '2025/Bring_Your_Own_Model.jpg', g: 'AI · Workshop', d: 'A hands-on low-technology workshop that teaches participants to build and train their own AI models.', v: 'Exhibition' },
    { t: 'Terms Of Confession', h: '2025/Terms_Of_Confession.html', i: '2025/Terms_Of_Confession.jpg', g: 'Performance · Data', d: 'A data-privacy performance that turns the act of agreeing to terms of service into a live, theatrical confessional ritual.', v: 'Personal project' },
    { t: 'OHL Plants',          h: '2025/OHL_Plants.html',          i: '2025/OHL_Plants.jpg',          g: 'Sensor · Residency', d: 'A living sensor garden where plants act as an interactive medium.', v: 'Residency' },
    { t: 'Kamuna',              h: '2025/Kamuna.html',              i: '2025/Kamuna.jpg',              g: 'Web · Community', d: 'A web experience designed to simulate communication to Mars.', v: 'Team project' },
    { t: 'Interplanetary Texting', h: '2025/Interplanetary_Texting.html', i: '2025/Interplanetary_Texting.jpg', g: 'Speculative', d: 'A speculative communication tool that simulates the real-time delay of sending messages across interplanetary distances.', v: 'Personal project' }
  ]},
  { year: 2024, items: [
    { t: 'Voice Box',           h: '2024/voice_box.html',           i: '2024/voice_box.jpg',           g: 'Speech · Interface', d: 'An interactive installation that creates a real-time radio play with your voice clone and chosen storyline.', v: 'Personal project' },
    { t: 'Flatware Hardware Software Wetware', h: '2024/Flatware_Hardware_Software_Wetware.html', i: '2024/Flatware_Hardware_Software_Wetware.jpg', g: 'Performance · Exhibition', d: 'Installation art for the exhibition (A)I Tell You, You Tell Me.', v: 'Exhibition' },
    { t: 'Meme Me',             h: '2024/meme_me.html',             i: '2024/meme_me.jpg',             g: 'Internet · Generative', d: 'A meme generator that converts your photo in real time into a contextually aware meme.', v: 'Personal project' }
  ]},
  { year: 2023, items: [
    { t: 'Live Coding',         h: '2023/isle_of_coding.html',      i: '2023/isle_of_coding.jpg',      g: 'Performance · Music', d: 'An algorave performance.', v: 'Live event' },
    { t: 'If You Think You Are Sleeping', h: '2023/if_you_think_you_are_sleeping.html', i: '2023/if_you_think_you_are_sleeping.jpg', g: 'Video · Interactive', d: 'A remembrance for Peter Weibel.', v: 'Personal project' },
    { t: 'Berthold Leibinger',  h: '2023/berthold_leibinger.html',  i: '2023/berthold_leibinger.jpg',  g: 'Identity · Commission', d: 'A corporate generative identity system for the Berthold Leibinger Foundation, producing unique visual marks from institutional data.', v: 'Commission' }
  ]},
  { year: 2022, items: [
    { t: 'Taming AI',           h: '2022/taming_ai.html',           i: '2022/taming_ai.jpg',           g: 'AI · Exhibition', d: 'Part of the interview series, Taming AI.', v: 'Exhibition' },
    { t: 'Agents',              h: '2022/agents.html',              i: '2022/agents.jpg',              g: 'Software · Personal', d: 'Interactive art about emergent behaviours.', v: 'Personal project' },
    { t: 'Botcast',             h: '2022/botcast.html',             i: '2022/botcast.jpg',             g: 'Audio · Team', d: 'A bot-generated daily news podcast.', v: 'Team project' },
    { t: 'Berlin Stallwächter Party', h: '2022/berlin_stallwachter_party.html', i: '2022/berlin_stallwachter_party.jpg', g: 'Live · Visualisation', d: 'A VR visualisation for the Stallwächter Party in Berlin.', v: 'Commission' }
  ]},
  { year: 2019, items: [
    { t: 'Memory Holes',        h: '2019/memory_holes.html',        i: '2019/memory_holes.jpg',        g: 'Installation · AR', d: 'An AR app for Turkey, built from the city archives.', v: 'Personal project' }
  ]},
  { year: 2017, items: [
    { t: 'Bindu',               h: '2017/bindu.html',               i: '2017/bindu.jpg',               g: 'Generative · VR', d: 'A VR app on the life of S.H. Raza.', v: 'Eyemyth Festival' },
    { t: 'Start Festival',      h: '2017/start_festival.html',      i: '2017/start_festival.jpg',      g: 'Identity · Commission', d: 'Start Festival installation.', v: 'Commission' },
    { t: 'Prayer Room',         h: '2017/prayer_room.html',         i: '2017/prayer_room.jpg',         g: 'Installation · Sacred', d: 'A VR tech installation.', v: 'Personal project' }
  ]},
  { year: 2016, items: [
    { t: 'Reflections',         h: '2016/reflections.html',         i: '2016/reflections.jpg',         g: 'Generative', d: 'A generative mirror portrait series in which a camera feed is continuously reimagined through layers of algorithmic transformation.', v: 'Personal project' }
  ]}
];

/* Flat, newest-first, with a running index — what the list renders. */
window.WC_FLAT = (function () {
  var out = [], n = 0;
  window.WC_WORKS.forEach(function (g) {
    g.items.forEach(function (it) {
      out.push({
        n: String(n++).padStart(2, '0'),
        year: g.year,
        title: it.t,
        href: it.h,
        img: it.i,
        tags: it.g,
        desc: it.d,
        venue: it.v
      });
    });
  });
  return out;
})();

/* Renders the index list into a container.
   opts: { base, limit, showDesc } */
window.WC_renderList = function (mount, opts) {
  opts = opts || {};
  var base = opts.base || window.WC_BASE || '';
  var rows = opts.limit ? window.WC_FLAT.slice(0, opts.limit) : window.WC_FLAT;

  mount.innerHTML = rows.map(function (w) {
    return '' +
      '<a class="wc-row" href="' + base + w.href + '"' +
      ' data-peek="' + base + w.img + '" data-say="Open">' +
      '<span class="wc-num">' + w.n + '</span>' +
      '<span class="wc-name">' + w.title + '</span>' +
      '<span class="wc-tags">' + w.tags + '</span>' +
      '<span class="wc-yr">' + w.year + '</span>' +
      '</a>';
  }).join('');
};
