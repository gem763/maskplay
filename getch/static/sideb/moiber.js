const guestboo = 363;

class Session {
  constructor() {
    this.page = {
      my:           { order: 0, instant: false, open: false },
      agit:         { order: 0, instant: false, open: false, boo: undefined, from: 'left' },
      researcher:     { order: 0, instant: false, open: false, from: 'left' },
      // finder:       { order: 0, instant: false, open: false, from: 'left', collections: undefined },
      collector:    { order: 0, instant: false, open: false, from: 'bottom', pix: undefined },
      signup:       { order: 0, instant: false, open: false, from: 'left' },
      // signup_email: { order: 0, instant: false, open: false, from: 'left', email: undefined },
      // signup_pw:    { order: 0, instant: false, open: false, from: 'left', email: undefined },
      login:        { order: 0, instant: false, open: false, from: 'left' },
      accountcheck: { order: 0, instant: false, open: false, from: 'left', existing: undefined },
      emailogin:    { order: 0, instant: false, open: false, from: 'left', email: undefined },
      emailsignup:  { order: 0, instant: false, open: false, from: 'left', email: undefined },
      texteditor:   { order: 0, instant: false, open: false, from: 'left', basetext: undefined, setter: undefined, placeholder: undefined, maxlines: 1 },
      pixeditor:    { order: 0, instant: false, open: false, from: 'left', src: undefined, pixloader: undefined, type: undefined },
      // profileconfig:{ order: 0, instant: false, open: false, from: 'left' },
      profiler:     { order: 0, instant: false, open: false, from: 'left', type: undefined },
      multichooser: { order: 0, instant: false, open: false, from: 'left', univ: undefined },

      // mbti:         { order: 0, instant: false, open: false, from: 'left', contents: undefined },
      mbtiresult:   { order: 0, instant: false, open: false, from: 'left', result: undefined, gender: undefined, mode: undefined },
      contentwork:  { order: 0, instant: false, open: false, from: 'left', contents: undefined },
      research:     { order: 0, instant: false, open: false, from: 'left', content: undefined },
      checkingame:  { order: 0, instant: false, open: false, from: 'top', researchitem: Checkingame.build(this) },

      stylevote:    { order: 0, instant: false, open: false, from: 'left', contents: undefined },
      search:       { order: 0, instant: false, open: false, from: 'left', category: 'pix' },
      brander:      { order: 0, instant: false, open: false, from: 'left', brand: undefined },

      about:        { order: 0, instant: true, open: false, from: 'left' },
      recruit:      { order: 0, instant: true, open: false, from: 'left' },
      policy:       { order: 0, instant: true, open: false, from: 'left' },
      privacy:      { order: 0, instant: true, open: false, from: 'left' },
      landing:      { order: 0, instant: true, open: false, from: 'left' },
      infoboard:    { order: 0, instant: true, open: false, from: 'right', contents: undefined },

      test:         { order: 0, instant: false, open: false, from: 'right' },
    };

    this.home = 'researcher';
    this.page[this.home].open = true;

    this.contentworks = {
      '동네스타일': Contentwork.build(this, { id: 1})
      // '동네스타일': Contentwork.build(this, { agenda: '동네스타일'})
    }

    this.store = new Store();
    this.editing = { on: false, selected:[] };
    this.pixtory = [{ pixs: new Pixs(this) }];
    this.scroll_direction = 'up';
    this.mode = { on: this.home, order: 0, prev: undefined };
    this.ikeyset = undefined;
    this.labels = undefined;
    this.entry = undefined;
    this.show_notice = undefined;
    this.researches = new Researches(this);
    this.supports = new Supports(this);
    this.shoptems = undefined;
    this.coffeecoupons = undefined;
    this.raffles = undefined;
    // this.checkingame = Checkingame.build(this);
    this.user = new User(this);

    this.dasher_control = undefined;
    // this.dasher_close = false;
    // setTimeout(()=>{this.user = new User(this);}, 10);
    // this.keyset_sampling();

    // this.open_brander(Brand.init(this, {id:2}));
    // this.open_test();
    // this.open_my();
    // this.open_profileconfig();
    // this.open_checkingame();
    this.open_multichooser();
  }

  // keyset_sampling() {
  //   this.ikeyset = _.sample([0, 1, 2]);
  // }

  refresh() {
    // this.keyset_sampling();
    this.pixtory = [{ pixs: new Pixs(this) }];
  }

  // keywording(keyword) {
  //   this.pixtory = [{ pixs: new Searchpixs_by_keyword(this, keyword) }];
  // }

  logout() {
    // this.expire();
    fetch('/logout/')
      .then(x => {
        if (x.ok) {
          location.reload();
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
    // this.page[this.mode.on].order = 0;
    this.checkout();

    if (this.mode.on in this.page) {
      this.page[this.mode.on].open = true;
      this.page[this.mode.on].order = this.mode.order;
    }
  }

  close_pages_all() {
    while (!this.on(this.home)) {
      this.close_page();
    }
  }

  open_page(pagename, covering) {
    if (this.on(pagename)) {
      return
    }

    if (pagename == this.home) {
      this.close_pages_all();
      return
    }

    if (this.on('researcher')) {
      covering = true;
    }

    if (!covering && this.mode.on in this.page) {
      this.page[this.mode.on].open = false;
      // this.page[this.mode.on].order = 0;

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

  on(...pages) {
    return !!pages.filter(p => this.mode.on == p).length
  }

  open_home() {
    this.open_page(this.home);
    // this.open_researcher();
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

  open_signup() {
    this.open_page('signup');
  }

  open_login() {
    this.open_page('login');
  }

  open_accountcheck(existing) {
    this.page.accountcheck.existing = existing;
    setTimeout(() => { this.open_page('accountcheck'); }, 10);
  }

  open_emailogin(email) {
    if (email) {
      this.page.emailogin.email = email;
    }
    this.open_page('emailogin');
  }

  open_emailsignup(email) {
    if (email) {
      this.page.emailsignup.email = email;
    }
    this.open_page('emailsignup');
  }

  open_my() {
    if (this.user.auth) {
      // this.open_page('my');
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

  open_researcher() {
    this.open_page('researcher');
  }

  open_search(pix) {
    if (pix) {
      this.pixtory.push({
        agenda: pix,
        pixs: new Searchpixs_by_pix(this, pix.id)
      });
    }

    this.open_page('search');
  }

  open_research(content) {
    this.page.research.content = content;
    this.open_page('research');
  }

  open_checkingame() {
    this.open_page('checkingame');
  }

  open_brander(brand) {
    this.page.brander.brand = brand;
    // this.page.brander.ready = false;
    this.open_page('brander');
  }

  open_stylevote() {
    if (!this.page.stylevote.contents) {
      this.page.stylevote.contents = new PixpairSet(this, 1000);
    }

    setTimeout(() => { this.open_page('stylevote'); }, 10);
  }

  open_collector(pix) {
    this.page.collector.pix = pix;
    this.open_page('collector', true);
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
    }

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

  // open_profileconfig() {
  //   this.open_page('profileconfig');
  // }

  open_multichooser(univ) {
    this.page.multichooser.univ = univ;
    this.open_page('multichooser');
  }

  open_profiler(type) {
    if (type) {
      this.page.profiler.type = type;

    } else {
      this.page.profiler.type = undefined;
    }

    this.open_page('profiler');
  }

  open_test() {
    this.open_page('test');
  }

  contact() {
    window.open('mailto:contact@moiber.com')
  }

  load_shoptems() {
    this.shoptems = new Shoptems(this);
  }

  load_raffles() {
    this.raffles = new Raffles(this);
  }

  load_coffeecoupons() {
    this.coffeecoupons = new Coffeecoupons(this);
  }
}







class Loader {
  constructor(session, baseobj) {
    this.session = session;
    this.onloading = false;
    // this.onloading = true;
    this.loaded = false;
    this.id = undefined;
    this.url = undefined;
    Object.assign(this, baseobj);
  }

  assign(obj) {
    Object.assign(this, obj);
  }

  load() {
    if (!this.loaded) {
      this.onloading = true;

      fetch(this.url)
        .then(x => x.json())
        .then(js => {
          this.onloading = false;
          this.loaded = true;

          if (js.success) {
            this.assign(js.content);
          }
        });
    }

    return this
  }

  // 객체만 생성 (로드는 안하기)
  static init(session, baseobj) {
    return new this(session, baseobj)
  }

  // 완전히 로드하기
  static build(session, baseobj) {
    return this.init(session, baseobj).load()
  }
}



class Pix extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/pix/${baseobj.id}`;
    this.desc = undefined;
    this.src = undefined;
    this.owner = undefined;
    this.outlink = undefined;
  }

  assign(obj) {
    this.desc = obj.desc;
    this.src = obj.src;
    this.outlink = obj.outlink;
    this.owner = Baseboo.init(this.session, obj.owner);
  }

  static init(session, baseobj) {
    if (baseobj.id in session.store.pixstore) {
      return session.store.pixstore[baseobj.id]

    } else {
      const pix = super.init(session, baseobj);
      Vue.set(session.store.pixstore, pix.id, pix);
      return pix
    }
  }
}


class Baseboo extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/boo/${baseobj.id}/baseboo`;
    this.text = undefined;
    this.profile = undefined;
    this.collections = undefined;
    // this.collections = new Collections(session, baseobj.id);
  }

  assign(obj) {
    // this.text = obj.text;
    // this.profile = obj.profile;
    // super.assign(abj);
    Object.assign(this, obj);
    this.collections = new Collections(this.session, this.id);
  }

  static init(session, baseobj) {
    if (baseobj.id in session.store.boostore) {
      return session.store.boostore[baseobj.id]

    } else {
      const boo = super.init(session, baseobj);
      Vue.set(session.store.boostore, boo.id, boo);
      return boo
    }
  }
}


class Boo extends Baseboo {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.voting_record = undefined;
    this.genderlabels = [];
    this.agelabels = [];
    this.stylelabels = [];
    this.itemlabels = [];
    this.styleprofile = {};
    // this.contentwork_result = {};
    this.rewarder = undefined;
    this.researched = [];
  }

  static init(session, baseobj) {
    const boo = super.init(session, baseobj);
    Vue.set(session.store.boostore, boo.id, boo);
    return boo
  }

  assign(obj) {
    Object.assign(this, obj);
    this.rewarder = new Rewarder(obj.rewards);
    this.collections = new Collections(this.session, this.id);
    delete this['rewards'];
  }


  get profiling_ready() {
    return this.rewarder!=undefined
  }


  stylevote(ipix_pos, ipix_neg, type) {
    if (!this.rewarder) {
      return
    }

    fetch(`stylevote?ipix_pos=${ipix_pos}&ipix_neg=${ipix_neg}&type=${type}`)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          // this.styleprofile.yourbrands = js.styleprofile.yourbrands;
          // this.styleprofile.scores = js.styleprofile.scores;
        }
      });

      if (type == 'clear') {
        this.rewarder.settle(-1, 'vote');

      } else if (type == 'new') {
        this.rewarder.settle(1, 'vote');
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

  make_collection(callback) {
    if (!this.collections) {
      return
    }

    this.session.open_texteditor('', '옷장이름을 입력해주세요', 1, txt_done => {
      const col = {
        id: undefined,
        name: txt_done,
        picks: new Picks(this.session),
        pixids: []
      }

      this.collections.list.unshift(col);
      if (callback) { callback(); }

      // this.cols.unshift(col);
      fetch(`/collection/create/${col.name}`)
        .then(x => x.json())
        .then(js => {
          if (js.success) {
            col.id = js.collection_id;
          }
        })
    });
  }
}

class Rewarder {
  constructor(rewards) {
    this.rewards = rewards;
    this.on_settling = false;
    this.reward_amount_max_daily = 100;
    this.reward_per_vote = 1;
    this.reward_per_collect = 1;
    this.reward_per_checkin = 10;
    this.reward_welcome = 500;
    this.reward_to_levelup = 2500;
  }

  settle(n, by) {
    let reward_change;
    let param_n, param_reward;

    if (by == 'vote') {
      reward_change = n * this.reward_per_vote;
      param_n = 'n_voted';
      param_reward = 'vote_reward';

    } else if (by == 'collect') {
      reward_change = n * this.reward_per_collect;
      param_n = 'n_collected';
      param_reward = 'collect_reward';
    }

    reward_change = Math.min(this.rewards.today.reward + reward_change, this.reward_amount_max_daily) - this.rewards.today.reward;

    this.rewards.today.n_action += n;
    this.rewards.total.n_action += n;
    this.rewards.today.reward += reward_change;
    this.rewards.total.reward += reward_change;
    this.on_settling = true;

    fetch(`settle?${param_n}=${n}&${param_reward}=${reward_change}`)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          this.on_settling = false;
          console.log(js);
        }
      });
  }

  settle_amount(amount, by) {
    this.on_settling = true;
    // this.rewards.today.reward += amount;
    this.rewards.total.reward += amount;

    let param_reward;

    if (by == 'checkin') {
      param_reward = 'checkin_reward';

    } else if (by == 'bonus') {
      param_reward = 'bonus_reward';
    }

    fetch(`settle?${param_reward}=${amount}`)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          this.on_settling = false;
          console.log(js);
        }
      });
  }
}


class Contentwork extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/contentwork/${baseobj.id}`;
    this.agenda = undefined;
    this.profiles = undefined;
    this.postages = new Postages(session, baseobj.id);
  }
}


class Collection extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/collection/${baseobj.id}`;
    this.name = undefined;
    this.pixids = undefined;
    this.owner = undefined;
    this.picks = undefined;
  }

  assign(obj) {
    this.name = obj.name;
    this.pixids = obj.pixids;
    this.owner = Baseboo.init(this.session, obj.owner);
    this.picks = new Picks(this.session, this.id);
  }
}


class Pick extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/pick/${baseobj.id}`;
    this.pix = undefined;
  }

  assign(obj) {
    this.pix = Pix.init(this.session, obj.pix);
  }
}


class Postage extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/postage/${baseobj.id}`;
    this.group = undefined;
  }
}


class ResearchItem extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/research/item/${baseobj.id}`;
    this.order = undefined;
    this.type = undefined;
    this.gender = undefined;
    this.preq = undefined;
    this.question = undefined;
    this.pix = undefined;
    this.mc = undefined;
    // this.pix_0 = undefined;
    // this.pixlabel_0 = undefined;
    // this.pix_1 = undefined;
    // this.pixlabel_1 = undefined;
  }
}


class Checkingame extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/research/checkingame`;
    this.order = undefined;
    this.type = undefined;
    this.gender = undefined;
    this.preq = undefined;
    this.question = undefined;
    this.pix = undefined;
    this.mc = undefined;
  }
}


class Item extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/item/${baseobj.id}`;
    // this.name = undefined;
    // this.price = undefined;
    // this.pix_0 = undefined;
    this.pix_1 = undefined;
    this.pix_2 = undefined;
    this.pix_3 = undefined;
    this.pix_4 = undefined;
    this.desc = undefined;
    // this.out_of_stock = undefined;
  }

  static init(session, baseobj) {
    if (baseobj.id in session.store.itemstore) {
      return session.store.itemstore[baseobj.id]

    } else {
      const item = super.init(session, baseobj);
      Vue.set(session.store.itemstore, item.id, item);
      return item
    }
  }
}


class Raffle extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/raffle/${baseobj.id}`;
    this.item = undefined;
    this.deduction = undefined;
    this.due = undefined;
    this.wallet = undefined;
  }

  assign(obj) {
    this.item = Item.init(this.session, obj.item);
    this.deduction = obj.deduction;
    this.due = obj.due;
    this.wallet = obj.wallet;
  }
}


class Coffeecoupon extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/coffeecoupon/${baseobj.id}`;
    this.item = undefined;
  }

  assign(obj) {
    this.item = Item.init(this.session, obj.item);
  }
}


class Shoptem extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/shoptem/${baseobj.id}`;
    this.item = undefined;
  }

  assign(obj) {
    this.item = Item.init(this.session, obj.item);
  }
}

// class Support extends Loader {
//   constructor(session, baseobj) {
//     super(session, baseobj);
//     this.url = `/support/${baseobj.id}`;
//     this.ticketsize = undefined;
//     this.target = undefined;
//     this.desc = undefined;
//     this.due = undefined;
//     this.gift = undefined;
//     this.active = undefined;
//   }
// }


class Brand extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/brand/${baseobj.id}`;
    // this.name_en = undefined;
    // this.name_kr = undefined;
    // this.logo = undefined;
    // this.homepage = undefined;
    // this.insta = undefined;
    // this.facebook = undefined;
    // this.youtube = undefined;
    this.origin = undefined;
    this.established = undefined;
    this.desc = undefined;
    this.coverpix_0 = undefined;
    this.coverpix_1 = undefined;
    this.coverpix_2 = undefined;
    this.coverpix_3 = undefined;
    this.coverpix_4 = undefined;
    // this.supports = undefined;
    this.researches = [];
    this.supports = [];
  }

  // assign(obj) {
  //   Object.assign(this, obj);
  //   this.supports = new Supports(this.session, this.id);
  // }

  static init(session, baseobj) {
    if (baseobj.id in session.store.brandstore) {
      return session.store.brandstore[baseobj.id]

    } else {
      const brand = super.init(session, baseobj);
      Vue.set(session.store.brandstore, brand.id, brand);
      return brand
    }
  }
}


class Research extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/research/${baseobj.id}`;
    this.owner = undefined;
    this.brand = undefined;
    this.title = undefined;
    this.desc = undefined;
    this.published = undefined;
    this.coverpix = undefined;
    this.reward = undefined;
    this.due = undefined;
    this.created_at = undefined;
    this.answers = undefined;
    this.researchitems = new ResearchItems(session, baseobj.id);
  }

  assign(obj) {
    this.owner = Baseboo.init(this.session, obj.owner);
    // this.brand = obj.brand ? Brand.init(this.session, obj.brand) : obj.brand;
    // this.brand = obj.brand;
    this.title = obj.title;
    this.desc = obj.desc;
    this.published = obj.published;
    this.coverpix = obj.coverpix;
    this.reward = obj.reward;
    this.due = obj.due;
    this.created_at = obj.created_at;
    this.answers = obj.answers;

    if (obj.brand) {
      this.brand = Brand.init(this.session, obj.brand);
      this.brand.researches.push(this);
    }
  }
}

class Support extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/support/${baseobj.id}`;
    this.brand = undefined;
    this.ticketsize = undefined;
    this.target = undefined;
    this.desc = undefined;
    this.due = undefined;
    this.gift = undefined;
    this.active = undefined;
    this.wallet = undefined;
  }

  assign(obj) {
    Object.assign(this, obj);
    // this.brand = obj.brand ? Brand.init(this.session, obj.brand) : obj.brand;
    if (obj.brand) {
      this.brand = Brand.init(this.session, obj.brand);
      this.brand.supports.push(this);
    }
  }
}


class Multiloader {
  constructor(session) {
    this.session = session;
    this.ids_url = undefined;
    this.ids = [];
    this.list = [];
    this.onloading = false;
    this.contentype;
    this.list_onloading = [];
  }

  load(n) {
    if (this.ids.length == 0) { return }
    if (n == 0) { return }
    if (!n) { var n = 1; }
    n = Math.min(n, this.ids.length);

    this.list_onloading = [];
    let _id;

    for (let i = 0; i < n; i++) {
      _id = this.ids.shift();
      // const content = this.contentype.build(this.session, { id:_id })

      if (_.findIndex(this.list, ['id', _id]) == -1) {
        const content = this.contentype.build(this.session, { id:_id });
        this.list.push(content);
        this.list_onloading.push(content);
      }
    };

    return this
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


class Raffles extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Raffle;
    this.nloads_init = 10;
    this.ids_url = `/raffle/iraffles`;
    this.load_ids();
  }
}


class Coffeecoupons extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Coffeecoupon;
    this.nloads_init = 10;
    this.ids_url = `/coffeecoupon/icoffeecoupons`;
    this.load_ids();
  }
}


class Shoptems extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Shoptem;
    this.nloads_init = 10;
    this.ids_url = `/shoptem/ishoptems`;
    this.load_ids();
  }
}

// class Supportbrands extends Multiloader {
//   constructor(session) {
//     super(session);
//     this.contentype = Brand;
//     this.nloads_init = 10;
//     this.ids_url = `/brand/isupportbrands`;
//     this.load_ids();
//   }
// }

class Supports extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Support;
    this.nloads_init = 100; // 우선 많이 받아오는데,, 나중에 이걸 바꿔야한다
    this.ids_url = `/support/isupports`;
    this.load_ids();
  }
}

// class Supports extends Multiloader {
//   constructor(session, brand_id) {
//     super(session);
//     this.contentype = Support;
//     this.nloads_init = 0;
//     this.ids_url = `/brand/${brand_id}/isupports`;
//     this.load_ids();
//   }
// }


class ResearchItems extends Multiloader {
  constructor(session, research_id) {
    super(session);
    this.contentype = ResearchItem;
    this.nloads_init = 0;
    this.ids_url = `/research/${research_id}/iresearchitems`;
    this.load_ids();
  }

  load_all() {
    this.load(this.ids.length);
  }
}


class Researches extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Research;
    this.nloads_init = 100;
    this.ids_url = `/research/iresearches`;
    this.load_ids();
  }

  // load_onworks() {
  //   this.onloading = true;
  //   fetch('/research/iresearches/onwork')
  //     .then(x => x.json())
  //     .then(js => {
  //       this.onloading = false;
  //
  //       if (js.success) {
  //         this.ids = js.ids.concat(this.ids);
  //         this.load(js.ids.length);
  //       }
  //     });
  // }
}


class Pixs extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `/pix/ipixs`;
    this.load_ids();
  }
}


class Searchpixs_by_pix extends Multiloader {
  constructor(session, pix_id) {
    super(session);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/pix/${pix_id}`;
    this.load_ids();
  }
}


class Searchpixs_by_keyword extends Multiloader {
  constructor(session, keyword) {
    super(session);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/keyword/${keyword}`;
    this.load_ids();
  }
}

class Searchpixs_by_collection extends Multiloader {
  constructor(session, collection_id) {
    super(session);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/collection/${collection_id}`;
    this.load_ids();
  }
}

class Picks extends Multiloader {
  // constructor(session, collection_id, nloads_init) {
  constructor(session, collection_id) {
    super(session);
    this.contentype = Pick;
    this.nloads_init = 1;
    // this.nloads_init = nloads_init;

    if (collection_id) {
      this.ids_url = `/collection/${collection_id}/ipicks`;
      this.load_ids();
    }
  }
}

class Collections extends Multiloader {
  constructor(session, owner_id) {
    super(session);
    this.contentype = Collection;
    this.nloads_init = 12;

    if (owner_id) {
      this.ids_url = `/boo/${owner_id}/icollections`;

    } else {
      this.ids_url = `/collection/icols`;
    }

    this.load_ids();
  }
}

class Postages extends Multiloader {
  constructor(session, contentwork_id) {
    super(session);
    this.contentype = Postage;
    this.nloads_init = 20;
    this.ids_url = `/contentwork/${contentwork_id}/ipostages`;
    this.load_ids();
  }
}

class Pixpair extends Multiloader {
  constructor(session, baseobj) {
    super(session);
    this.contentype = Pix;
    this.ids = baseobj.id;
    // this.load(2);
  }

  static build(session, baseobj) {
    return new this(session, baseobj).load(2)
  }
}

class PixpairSet extends Multiloader {
  constructor(session, n) {
    super(session);
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
    this.brandstore = {};
    this.itemstore = {};
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
        if (js.success) {
          this.auth = new Auth(js.user, this.session);
          // this.session.open_profileconfig();

          // if (js.user.is_superuser) {
          //   this.session.researches.load_onworks();
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

  get auth_ready() {
    if (this.has_auth) {
      return this.boo.loaded
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
  // constructor(cuser, store) {
  constructor(cuser, session) {
    this.id = Number(cuser.id);
    // this.store = store;
    this.session = session;
    this.email = cuser.email;
    this.is_superuser = cuser.is_superuser;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.build(session, cuser.boo)} : {};
    // this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.build(cuser.boo.id, store)} : {};
    // this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.rebuild(cuser.boo, store, true)} : {};
    this.boos_fully_loaded = false;
    // this.links = cuser.links;
    // this.load_other_boos();
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
    this.boos[this.boo_selected] = Boo.build(this.session, this.boos[this.boo_selected]);
    // this.boos[this.boo_selected] = Boo.build(this.boo_selected, this.store);
    // this.boos[this.boo_selected] = Boo.rebuild(this.boos[this.boo_selected], this.store, true);
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
