const guestboo = 363;

class Session {
  constructor() {
    this.page = {
      my:           { order: 0, instant: false, open: false },
      agit:         { order: 0, instant: false, open: false, boo: undefined, from: 'left' },
      research:     { order: 0, instant: false, open: true, from: 'left' },
      // finder:       { order: 0, instant: false, open: false, from: 'left', collections: undefined },
      collector:    { order: 0, instant: false, open: false, from: 'bottom', pix: undefined },
      login:        { order: 0, instant: false, open: false, from: 'left' },
      texteditor:   { order: 0, instant: false, open: false, basetext: undefined, setter: undefined, placeholder: undefined, maxlines: 1 },
      pixeditor:    { order: 0, instant: false, open: false, src: undefined, pixloader: undefined, type: undefined },
      profiler:     { order: 0, instant: false, open: false, from: 'left', type: undefined },

      // mbti:         { order: 0, instant: false, open: false, from: 'left', contents: undefined },
      mbtiresult:   { order: 0, instant: false, open: false, from: 'left', result: undefined, gender: undefined, mode: undefined },
      contentwork:  { order: 0, instant: false, open: false, from: 'left', contents: undefined },

      stylevote:    { order: 0, instant: false, open: false, from: 'left', contents: undefined },
      search:       { order: 0, instant: false, open: false, from: 'left', category: 'pix' },

      about:        { order: 0, instant: true, open: false, from: 'left' },
      recruit:      { order: 0, instant: true, open: false, from: 'left' },
      policy:       { order: 0, instant: true, open: false, from: 'left' },
      privacy:      { order: 0, instant: true, open: false, from: 'left' },
      landing:      { order: 0, instant: true, open: false, from: 'left' },
      infoboard:    { order: 0, instant: true, open: false, from: 'right', contents: undefined },
    };

    this.contentworks = {
      '동네스타일': new Contentwork('동네스타일')
    }

    this.store = new Store();
    this.editing = { on: false, selected:[] };
    this.pixtory = [{ pixs: new Pixs(this.store) }];
    this.scroll_direction = 'up';
    this.mode = { on: 'research', order: 0, prev: undefined };
    this.ikeyset = undefined;
    this.labels = undefined;
    this.entry = undefined;
    this.show_notice = undefined;
    this.user = new User(this);
    // this.keyset_sampling();
  }

  // keyset_sampling() {
  //   this.ikeyset = _.sample([0, 1, 2]);
  // }

  refresh() {
    // this.keyset_sampling();
    this.pixtory = [{ pixs: new Pixs(this.store) }];
  }

  keywording(keyword) {
    this.pixtory = [{ pixs: new Searchpixs_by_keyword(this.store, keyword) }];
    // this.pixtory.push({ pixs: new Searchpixs_by_keyword(this.store, keyword) });
  }

  logout() {
    this.close_page();
    this.expire();

    fetch('/logout/')
      .then(x => {
        if (x.ok) {
          console.log('successfully logged out');
        }
      });
  }

  expire() {
    // auth만 제거하고, guest는 상주하게 한다
    this.user.auth = undefined;
  }

  close_page() {
    this.page[this.mode.on].open = false;
    this.page[this.mode.on].order = 0;
    this.checkout();

    if (this.mode.on in this.page) {
      this.page[this.mode.on].open = true;
      this.page[this.mode.on].order = this.mode.order;
    }
  }

  close_pages_all() {
    while (this.mode.on!='research') {
      this.close_page();
    }
  }

  open_page(pagename) {
    if (pagename == this.mode.on) {
      return
    }

    if (this.mode.on in this.page) {
      this.page[this.mode.on].open = false;
      this.page[this.mode.on].order = 0;

      if (this.page[this.mode.on].instant) {
        this.checkout();
      }
    }

    this.checkin(pagename);
    this.page[pagename].open = true;
    this.page[pagename].order = this.mode.order;
  }

  checkin(on) {
    console.log(`check-in to ${on}`);
    this.mode.prev = {...this.mode};
    this.mode.on = on;
    this.mode.order = this.mode.prev.order + 1;
  }

  checkout() {
    try {
      console.log(`check-out from ${this.mode.on}, back to ${this.mode.prev.on}`)
      this.mode = this.mode.prev;

    } catch(e) {
      console.log('abnormal access')
    }
  }

  // open_home(pix) {
  //   if (pix) {
  //     pix.load_owner();
  //
  //     this.pixtory.push({
  //       agenda: pix,
  //       pixs: new Searchpixs_by_pix(this.store, pix.id)
  //     });
  //   }
  //
  //   this.close_pages_all();
  // }


  open_home() {
    this.open_research();
  }

  open_about() {
    this.open_page('about');
  }

  open_infoboard(position) {
    this.page.infoboard.contents = position;
    this.open_page('infoboard');
  }

  open_recruit() {
    this.open_page('recruit');
  }

  open_policy() {
    this.open_page('policy');
  }

  open_privacy() {
    this.open_page('privacy');
  }

  open_landing() {
    this.open_page('landing');
  }

  open_login() {
    this.open_page('login');
  }

  open_my() {
    if (this.user.auth) {
      this.open_agit(this.user.boo);

    } else {
      this.open_login();
    }
  }

  open_agit(boo) {
    this.page.agit.boo = boo;
    // agit 최초 오픈시 처음에는 boo=undefined 이기 때문에,
    // 열림효과가 제대로 반영하기 위해 약간 딜레이를 줬다
    setTimeout(() => { this.open_page('agit'); }, 10);
  }

  // open_finder() {
  //   this.open_page('finder');
  // }

  open_research() {
    this.open_page('research');
  }

  open_search(pix) {
    if (pix) {
      pix.load_owner();

      this.pixtory.push({
        agenda: pix,
        pixs: new Searchpixs_by_pix(this.store, pix.id)
      });
    }

    this.open_page('search');
  }

  open_stylevote() {
    if (!this.page.stylevote.contents) {
      this.page.stylevote.contents = new PixpairSet(this.store, 1000);
    }

    setTimeout(() => { this.open_page('stylevote'); }, 10);
  }

  open_collector(pix) {
    this.page.collector.pix = pix;
    this.open_page('collector');
  }

  open_texteditor(basetext, placeholder, maxlines, setter) {
    this.page.texteditor.basetext = basetext;
    this.page.texteditor.placeholder = placeholder;
    this.page.texteditor.setter = setter;
    this.page.texteditor.maxlines = maxlines;
    this.open_page('texteditor');
  }

  open_pixeditor(src, type, pixloader) {
    this.page.pixeditor.src = src;
    this.page.pixeditor.type = type;
    this.page.pixeditor.pixloader = pixloader;
    this.open_page('pixeditor');
  }

  open_contentwork(agenda) {
    if (!this.page.contentwork.contents) {
      this.page.contentwork.contents = this.contentworks[agenda];
      // this.page.contentwork.contents = new Contentwork(agenda);
    }

    // this.close_pages_all();
    // this.open_page('contentwork');
    setTimeout(() => { this.open_page('contentwork'); }, 10);
  }

  open_mbtiresult(agenda, result, gender, mode) {
    if (!this.page.contentwork.contents) {
      this.page.contentwork.contents = this.contentworks[agenda];
    }

    this.page.mbtiresult.result = result;
    this.page.mbtiresult.gender = gender;
    this.page.mbtiresult.mode = mode;
    this.open_page('mbtiresult');
  }

  open_profiler(type) {
    if (type) {
      this.page.profiler.type = type;

    } else {
      this.page.profiler.type = undefined;
    }

    this.open_page('profiler');
  }
}


class Loader {
  constructor(id, store) {
    this.id = id;
    this.store = store;
    this.onloading = true;
  }

  assign(js) {
    Object.assign(this, js.content);
  }

  load() {
    fetch(this.url(this.id))
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          this.assign(js);
          // Object.assign(this, js.content);
        }
      });
  }
}

class Pix extends Loader {
  constructor(id, store) {
    if (id in store.pixstore) {
      return store.pixstore[id]

    } else {
      super(id, store);
      store.pixstore[this.id] = this;
      this.url = (id) => `/pix/${id}`;
      this.desc = undefined;
      this.src = undefined;
      this.owner = undefined;
      this.outlink = undefined;
      this.load();
    }
  }

  assign(js) {
    this.desc = js.content.desc;
    this.src = js.content.src;
    this.outlink = js.content.outlink;
    this.owner = new Boo(js.content.owner.id, this.store);
    this.owner.nick = js.content.owner.nick;
    this.owner.collections = js.content.owner.collections;
  }

  load_owner() {
    this.owner = Boo.rebuild(this.owner, this.store);
  }
}

class Boo extends Loader {
  constructor(id, store) {
    if (id in store.boostore) {
      return store.boostore[id]

    } else {
      super(id, store);
      store.boostore[this.id] = this;
      this.url = (id) => `/boo/${id}/baseboo`;
      this.text = undefined;
      this.profile = undefined;
      this.active = undefined;
      this.voting_record = undefined;
      this.genderlabels = [];
      this.agelabels = [];
      this.stylelabels = [];
      this.itemlabels = [];
      this.styleprofile = {};
      this.rewards = {};
      this.contentwork_result = {};

      this.on_settling = false;
      this.reward_n_cycle = 10;
      this.reward_amount_sub = 10;
      this.reward_amount_max = 100;
      this.reward_to_levelup = 2500;
      this.load();
    }
  }

  static rebuild(baseboo, store, is_auth) {
    const nick = baseboo.nick;
    const collections = baseboo.collections;
    const _boo = new Boo(baseboo.id, store);
    _boo.evolute(nick, collections, is_auth);
    return _boo
  }

  get profiling_ready() {
    return Object.keys(this.rewards).length > 0
    // return (Object.keys(this.rewards).length > 0) && (Object.keys(this.styleprofile).length > 0)
  }

  stylevote(ipix_pos, ipix_neg, type) {
    fetch(`stylevote?ipix_pos=${ipix_pos}&ipix_neg=${ipix_neg}&type=${type}`)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          // console.log(js.styleprofile);
          // this.styleprofile.yourbrands = js.styleprofile.yourbrands;
          // this.styleprofile.scores = js.styleprofile.scores;
        }
      });

      if (type == 'clear') {
        this.settle(-1, 'vote');

      } else if (type == 'new') {
        this.settle(1, 'vote');
      }
  }

  settle_amount(amount, by) {
    this.rewards.today.reward += amount;
    this.rewards.total.reward += amount;

    let param_reward;

    if (by == 'checkin') {
      param_reward = 'checkin_reward';

    } else if (by == 'bonus') {
      param_reward = 'bonus_reward';
    }

    this.on_settling = true;
    const url = `settle?${param_reward}=${amount}`
    // console.log(url);
    fetch(url)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          this.on_settling = false;
          console.log(js);
        }
      });
  }

  settle(n, by) {
    // if (Object.keys(this.rewards).length === 0 && this.rewards.constructor === Object) {
    //   console.log('아직 rewards 객체가 생성되지 않음');
    // }
    let reward_change;
    let param_n, param_reward;

    this.rewards.today.n_action += n;
    this.rewards.total.n_action += n;

    if (this.rewards.today.n_action % this.reward_n_cycle == 0) {
      reward_change = this.reward_amount_sub;

    } else {
      reward_change = 0;
    }
    // reward_change = parseInt(this.rewards.today.n_action / this.reward_n_cycle) * this.reward_amount_sub - this.rewards.today.reward;

    this.rewards.today.reward += reward_change;
    this.rewards.total.reward += reward_change;

    if (by == 'vote') {
      param_n = 'n_voted';
      param_reward = 'vote_reward';

    } else if (by == 'collect') {
      param_n = 'n_collected';
      param_reward = 'collect_reward';
    }

    // fetch(`settle?n_voted=${n}&vote_reward=${reward_change}`)
    this.on_settling = true;
    const url = `settle?${param_n}=${n}&${param_reward}=${reward_change}`
    // console.log(url);
    fetch(url)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          this.on_settling = false;
          console.log(js);
        }
      });
  }

  evolute(nick, collections, is_auth) {
    if (!this.nick) {
      this.nick = nick;
    }

    if (!this.collections) {
      // collections = collections.map(...) 으로 하면 안된다
      // 새로운 객체 new Picks(...)에 Vue가 reactive하지 못하다
      // collections.forEach(col => {
      //   if (!col.picks)
      //     Vue.set(col, 'picks', new Picks(this.store, col.id));
      // });
      //
      // this.collections = collections;

      this.collections = collections.map(col => {
        if (!col.picks) {
          const _col = is_auth ? new Collection(col.id, this.store) : new CollectionBase(col.id, this.store);
          _col.name = col.name;
          return _col

        } else {
          return col
        }
      });
      // this.collections = collections;
    }
  }

  has_pix(pix_id, collection) {
    if (collection) {
      if (collection.pixids) {
        return collection.pixids.includes(pix_id)
      }
      return false

    } else if (this.collections) {
      return _.findIndex(this.collections, function(o) {
        if (o.pixids) {
          return o.pixids.includes(pix_id)
        }
        return false
      }) > -1;
    }
  }
}


class Contentwork extends Loader {
  constructor(agenda) {
    super(undefined, undefined);
    this.url = (agenda) => `/contentwork/${agenda}`;
    this.agenda = agenda;
    this.profiles = undefined;
    this.postages = new Postages(undefined, agenda);
    this.load();
  }

  load() {
    fetch(this.url(this.agenda))
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          Object.assign(this, js.content);
        }
      });
  }
}


class Collection extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/collection/${id}`;
    this.owner = undefined;
    this.pixids = undefined;
    this.picks = new Picks(this.store, id, 6);
    this.load();
  }

  load_owner() {
    this.owner = Boo.rebuild(this.owner, this.store, true);
  }
}

class CollectionBase extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/collection/${id}/base`;
    this.owner = undefined;
    // this.pixids = undefined;
    this.picks = new Picks(this.store, id, 1);
    this.load();
  }

  load_owner() {
    this.owner = Boo.rebuild(this.owner, this.store);
  }
}

class Pick extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/pick/${id}`;
    this.pix = undefined;
    this.load();
  }

  load() {
    fetch(this.url(this.id))
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          this.pix = new Pix(js.content.pix.id, this.store);
        }
      });
  }
}


class Post extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/post/${id}`;
    this.group = undefined;
    this.load();
  }
}

class Postage extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/postage/${id}`;
    this.group = undefined;
    this.load();
  }
}


class Multiloader {
  constructor(store) {
    this.store = store;
    this.ids = [];
    this.list = [];
    this.onloading = false;
    this.contentype = undefined;

    this.list_onloading = [];
  }

  load(n) {
    if (this.ids.length == 0) {
      return
    }

    if (!n) { var n = 1; }
    n = Math.min(n, this.ids.length);

    this.list_onloading = [];
    let _id;

    for (let i = 0; i < n; i++) {
      _id = this.ids.shift();
      const content = new this.contentype(_id, this.store)

      if (_.findIndex(this.list, ['id', _id]) == -1) {
        this.list.push(content);
        this.list_onloading.push(content);
      }
    };
  }

  load_ids() {
    this.onloading = true;
    fetch(this.ids_url)
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          this.ids = js.ids;
          this.load(this.nloads_init);
        }
      });
  }
}



class Pixs extends Multiloader {
  constructor(store) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `/pix/ipixs`;
    this.load_ids();
  }
}


class Searchpixs_by_pix extends Multiloader {
  constructor(store, pix_id) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/pix/${pix_id}`;
    this.load_ids();
  }
}


class Searchpixs_by_keyword extends Multiloader {
  constructor(store, keyword) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/keyword/${keyword}`;
    this.load_ids();
  }
}

class Searchpixs_by_collection extends Multiloader {
  constructor(store, collection_id) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/collection/${collection_id}`;
    this.load_ids();
  }
}

class Picks extends Multiloader {
  constructor(store, collection_id, nloads_init) {
    super(store);
    this.contentype = Pick;
    this.nloads_init = nloads_init;

    if (collection_id) {
      this.ids_url = `/collection/${collection_id}/ipicks`;
      this.load_ids();
    }
  }
}

class Collections extends Multiloader {
  constructor(store) {
    super(store);
    this.contentype = CollectionBase;
    this.nloads_init = 12;
    this.ids_url = `/collection/icols`;
    this.load_ids();
  }
}

class Mbti extends Multiloader {
  constructor(store, type) {
    super(store);
    this.contentype = Post;
    this.nloads_init = 20;
    this.ids_url = `/mbti/${type}/iposts`;
    this.load_ids();
  }
}

class Postages extends Multiloader {
  constructor(store, agenda) {
    super(store);
    this.contentype = Postage;
    this.nloads_init = 20;
    this.ids_url = `/contentwork/${agenda}/ipostages`;
    this.load_ids();
  }
}

class Pixpair extends Multiloader {
  constructor(candids, store) {
    super(store);
    this.contentype = Pix;
    this.ids = candids;
    this.load(2);
  }
}

class PixpairSet extends Multiloader {
  constructor(store, n) {
    super(store);
    this.contentype = Pixpair;
    this.nloads_init = 10;
    this.ids_url = `/pix/ipixs/comb/${n}`;
    this.load_ids();
  }
}


class Store {
  constructor() {
    this.pixstore = {};
    this.boostore = {};
  }
}


class User {
  constructor(session) {
    this.auth = undefined;
    this.guest = undefined;
    this.onloading = true;
    this.loginplz = false;
    this.session = session;
    this.load();
  }

  load() {
    fetch('/user2')
      .then(x => x.json())
      .then(js => {
        // console.log(js);

        if (js.success) {
          // console.log(js.user);
          this.auth = new Auth(js.user, this.session.store);
          // this.auth = new Auth(JSON.parse(js.user), this.session.store);

          // if (js.first_visit) {
          //   this.auth.first_visit = js.first_visit;
          //   this.session.open_profiler();
          // }
        }

        this.guest = { boo: JSON.parse(js.guestboo) };
        this.onloading = false;
      });
  }

  get has_auth() {
    return this.auth ? true : false
  }

  get is_guest() {
    return this.guest ? true : false
  }

  get boo() {
    if (this.has_auth) {
      return this.auth.boo

    } else if (this.is_guest){
      return this.guest.boo
    }
  }

  is_myboo(boo) {
    if (this.has_auth) {
      return this.auth.is_myboo(boo)
    }
  }

  is_following(boo) {
    return this.has_auth && !this.is_myboo(boo) && this.auth.is_following(boo.id)
  }

  follow(boo) {
    if (this.has_auth) {
      this.auth.follow(boo.id)
    }
  }

  unfollow(boo) {
    if (this.has_auth) {
      this.auth.unfollow(boo.id)
    }
  }

  get boos_fully_loaded() {
    if (this.has_auth) {
      return this.auth.boos_fully_loaded

    } else {
      return true
    }
  }

  contentvote(postage_id, action) {
    if (!this.boo) {
      return
    }

    const feed_act = {};
    feed_act[postage_id] = action;
    this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);

    fetch(`/postage/${postage_id}/contentvote?action=${action}`)
      .then(x => x.json())
      .then(js => {
        console.log(js);
      });
  }


  // vote(post_id, action) {
  //   if (!this.boo) {
  //     return
  //   }
  //
  //   const feed_act = {};
  //   feed_act[post_id] = action;
  //   this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);
  //
  //   fetch(`/post/${post_id}/vote?action=${action}`)
  //     .then(x => x.json())
  //     .then(js => {
  //       console.log(js);
  //     });
  // }

  has_voted_as(postage_id) {
    if (!this.boo)
      return -1

    if (!this.boo.voting_record)
      return -1

    if (postage_id in this.boo.voting_record) {
      return this.boo.voting_record[postage_id]

    } else {
      return -1
    }
  }

  has_liked_comment(comment_id) {
    if (this.boo)
      return this.boo.ilikes_comment.includes(comment_id)
  }

  like_comment(comment_id) {
    if (this.boo)
      this.boo.ilikes_comment.push(comment_id)
  }

  delike_comment(comment_id) {
    if (this.boo) {
      const where = this.boo.ilikes_comment.indexOf(comment_id);
      this.boo.ilikes_comment.splice(where, 1);
    }
  }
}


class Auth {
  constructor(cuser, store) {
    // console.log(cuser)
    this.id = Number(cuser.id);
    this.store = store;
    this.email = cuser.email;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.rebuild(cuser.boo, store, true)} : {};
    // this.boos = cuser.boo ? {[cuser.boo_selected]: cuser.boo} : {};
    this.boos_fully_loaded = false;
    this.links = cuser.links;
    // this.first_visit = false;
    this.load_other_boos();
  }

  is_myboo(boo) {
    return boo.id == this.boo_selected
  }

  api_get(url) {
    fetch(url)
      .then(x => x.json())
      .then(js => {
        console.log(js)
      });
  }

  load_other_boos() {
    fetch('/user2/other_boos')
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          // this.boos = { ...this.boos, ...JSON.parse(js.other_boos) };
          this.boos = { ...this.boos, ...js.other_boos };
          this.boos_fully_loaded = true;
        }
      })
  }

  set boo(boo_id) {
    if (this.boo) {
      console.log(`boo changed to [${boo_id}]${this.boos[boo_id].nick} from [${this.boo_selected}]${this.boo.nick}`);

    } else {
      console.log(`boo [${boo_id}]${this.boos[boo_id].nick} created at the first time`);
    }

    this.boo_selected = Number(boo_id);
    this.boos[this.boo_selected] = Boo.rebuild(this.boos[this.boo_selected], this.store, true);
    this.api_get(`/boo/${boo_id}/set/`);
  }

  get boo() {
    return this.boos[this.boo_selected];
  }

  is_following(author_id) {
    return this.boo.followees_id.includes(author_id);
  }

  unfollow(author_id) {
    this.api_get(`/boo/${author_id}/unfollow`);

    const where = this.boo.followees_id.indexOf(author_id);
    this.boo.followees_id.splice(where, 1);
  }

  follow(author_id) {
    this.api_get(`/boo/${author_id}/follow`);
    this.boo.followees_id.push(author_id);
  }

  // has_voted_as(post_id) {
  //   if (post_id in this.boo.voting_record) {
  //     return this.boo.voting_record[post_id]
  //
  //   } else {
  //     return -1
  //   }
  // }

  // has_liked_comment(comment_id) {
  //   return this.boo.ilikes_comment.includes(comment_id)
  // }
  //
  // like_comment(comment_id) {
  //   this.boo.ilikes_comment.push(comment_id)
  // }
  //
  // delike_comment(comment_id) {
  //   const where = this.boo.ilikes_comment.indexOf(comment_id);
  //   this.boo.ilikes_comment.splice(where, 1);
  // }

  // vote(post_id, action) {
  //   const feed_act = {};
  //   feed_act[post_id] = action;
  //   this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);
  //
  //   fetch(`/post/${post_id}/vote?action=${action}`)
  //     .then(x => x.json())
  //     .then(js => {
  //       console.log(js);
  //       this.boo.fit = js.fit;
  //     });
  // }
}
