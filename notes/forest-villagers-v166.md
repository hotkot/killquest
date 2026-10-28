# Forest villager introduction

Removed the elderwoman sprite, shadow, unused image preload and former plea. Replaced her with three existing frightened townsfolk (headscarf woman, teal-clad woman, older traveler), standing at normal NPC size during the three-second hero entrance and conversation.

Three dialogue pages: the two supplied shared villager lines, followed by one separate portrait/color window for each selected hero, using only that hero's supplied response. Canonical roster names Garran and Selene are retained. The viewport remains visible around the bottom conversation panels; response layout adapts from four columns on desktop to two on narrow screens. No scrolling text boxes.

Keyboard Enter/Space/J, controller jump/light and the shared Continue button advance the conversation. A0.25second input debounce prevents simultaneous co-op confirmations from skipping pages. The final confirmation is consumed, restores exploration, and releases the townsfolk to run off left. Returning to a level clears prior civilian views. Boss dialogue retains its own existing flow.

Verification: all15 nonempty subsets of the four heroes; exact script, selected-only replies, input consumption/debounce, locked movement/camera and stable civilian idle positions, departure/cleanup/restart, full Forest campaign route/boss entrance and normal test-level scene lifecycle. The real scene adapter verifies all1343 resources, DOM content/visibility and sprite animation changes. Browser layout was not visually verified in this update.
