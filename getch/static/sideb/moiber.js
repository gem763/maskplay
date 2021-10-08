const guestboo = 363;

class Session {
  constructor() {
    this.page = {
      my:           { order: 0, instant: false, open: false },
      agit:         { order: 0, instant: false, open: false, boo: undefined, from: 'left' },
      researcher:   { order: 0, instant: false, open: false, from: 'left' },
      collector:    { order: 0, instant: false, open: false, from: 'bottom', pix: undefined },
      baseinfo:     { order: 0, instant: false, open: false, from: 'left' },
      signup:       { order: 0, instant: false, open: false, from: 'left' },
      signupper:    { order: 0, instant: false, open: false, from: 'left' },
      login:        { order: 0, instant: false, open: false, from: 'left' },
      accountcheck: { order: 0, instant: false, open: false, from: 'left', existing: undefined },
      emailogin:    { order: 0, instant: false, open: false, from: 'left', email: undefined },
      emailsignup:  { order: 0, instant: false, open: false, from: 'left', email: undefined },
      texteditor:   { order: 0, instant: false, open: false, from: 'left', basetext: undefined, setter: undefined, placeholder: undefined, maxlines: 1 },
      pixeditor:    { order: 0, instant: false, open: false, from: 'left', src: undefined, pixloader: undefined, type: undefined },
      profiler:     { order: 0, instant: false, open: false, from: 'left', type: undefined },
      multichooser: { order: 0, instant: false, open: false, from: 'left', univ: undefined },

      // mbtiresult:   { order: 0, instant: false, open: false, from: 'left', result: undefined, gender: undefined, mode: undefined },
      // contentwork:  { order: 0, instant: false, open: false, from: 'left', contents: undefined },
      research:     { order: 0, instant: false, open: false, from: 'left', content: undefined },
      checkin:      { order: 0, instant: false, open: false, from: undefined },
      flashgames:   { order: 0, instant: false, open: false, from: 'top', content: undefined },

      stylevote:    { order: 0, instant: false, open: false, from: 'left'},// contents: new PixpairSet(this) },
      // stylevote:    { order: 0, instant: false, open: false, from: 'left', contents: new PixpairSet(this, 200) },
      search:       { order: 0, instant: false, open: false, from: 'left', category: 'pix' },
      brander:      { order: 0, instant: false, open: false, from: 'left', brand: undefined },

      about:        { order: 0, instant: true, open: false, from: 'left' },
      recruit:      { order: 0, instant: false, open: false, from: 'left' },
      policy:       { order: 0, instant: true, open: false, from: 'left' },
      privacy:      { order: 0, instant: true, open: false, from: 'left' },
      landing:      { order: 0, instant: true, open: false, from: 'left' },
      // zthinker:     { order: 0, instant: false, open: false, from: 'left' },
      bulletin:     { order: 0, instant: false, open: false, from: 'left', type: undefined },
      infoboard:    { order: 0, instant: true, open: false, from: 'right', contents: undefined },

      test:         { order: 0, instant: false, open: false, from: 'right' },
    };

    this.home = 'researcher';
    this.page[this.home].open = true;

    this.show_guider = false;
    // this.popup = { open: false, type: undefined, actions: {} };

    // this.contentworks = {
    //   '동네스타일': Contentwork.build(this, { id: 1})
    //   // '동네스타일': Contentwork.build(this, { agenda: '동네스타일'})
    // }

    this.store = new Store();
    this.editing = { on: false, selected:[] };
    this.pixtory = [{ pixs: new Pixs(this) }];
    this.scroll_direction = 'up';
    this.mode = { on: this.home, order: 0, prev: undefined, dasher_control: this.dasher_control };
    this.ikeyset = undefined;
    this.labels = undefined;
    this.entry = undefined;
    this.show_notice = undefined;
    this.researches = new Researches(this);
    this.supports = new Supports(this);
    this.flashgames = new Flashgames(this);
    this.shoptems = undefined;
    this.coffeecoupons = undefined;
    this.raffles = undefined;
    this.stylelabels = undefined; //new Stylelabels(this);
    this.itemlabels = undefined;
    // this.checkingame = Checkingame.build(this);
    this.balancegame = { pixpair_set: new PixpairSet(this), stat: undefined, stat_updated: false, stat_last: false };
    this.user = new User(this);
    // this.keyset_sampling();

    this.reload_everyday();
    // this.open_baseinfo();
    // this.open_signup();

    // fetch('balancegame/stat')
    //   .then(x => x.json())
    //   .then(js => {
    //     if (js.success) {
    //       this.balancegame.stat = js.stat;
    //       this.balancegame.stat_updated = true;
    //     }
    //   });
  }

  // reload_user() {
  //   this.user = new User(this);
  // }

  get dasher_control() {
    return {
      show: true,
      open: false,
      section: undefined,
      phase: 'menu',
      content: undefined,
      detail_obj: undefined
    }
  }

  reload_everyday() {
    const now = new Date();
    const night = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1, // the next day, ...
        0, 0, 0 // ...at 00:00:00 hours
    );

    var msTillMidnight = night.getTime() - now.getTime();
    setTimeout(() => {
      location.reload();
      // this.reload_everyday();

    }, msTillMidnight);
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

    this.mode.dasher_control = this.dasher_control;
  }

  open_page(pagename, covering) {
    if (this.on(pagename)) {
      setTimeout(() => {
        this.mode.dasher_control.open = false;
        this.mode.dasher_control.section = undefined;
      }, 200);
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
    this.mode.dasher_control = this.dasher_control;
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

  // open_guider() {
  //   this.open_page('guider');
  // }

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

  // open_zthinker() {
  //   this.open_page('zthinker');
  // }

  open_bulletin(type) {
    this.page.bulletin.type = type;
    this.open_page('bulletin');
  }

  open_baseinfo() {
    this.open_page('baseinfo');
  }

  open_signup() {
    this.open_page('signup');
  }

  open_signupper() {
    this.open_page('signupper');
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
    if (this.user.has_auth) {
      this.page.research.content = content;
      this.open_page('research');

    } else {
      const answer = confirm('서베이 참여로 포인트를 지급받으려면 로그인이 필요합니다');
      if (answer) {
        this.open_login();
      }
    }
  }


  open_checkin() {
    this.open_page('checkin');
  }


  open_flashgames() {
    if (this.user.has_auth) {
      if (this.user.boo.wallet) {
        if (!this.user.boo.wallet.checkin_today) {
          this.user.boo.wallet.receive('checkin_game', this.user.boo.wallet.per_checkin);
          this.user.boo.wallet.checkin_today = true;
          alert('<출첵> 지금 ' + this.user.boo.wallet.per_checkin + 'P가 지급되었습니다');

        } else {
          alert('출첵 포인트가 이미 지급되었습니다')
        }

      } else {
        // alert('')
      }

    } else {
      const yes = confirm('로그인 해주세요');
      if (yes) {
        this.open_login();
      }
      // alert('로그인 해주세요')
    }

  }


  // open_flashgames() {
  //   this.open_page('flashgames');
  // }

  open_brander(brand) {
    this.page.brander.brand = brand;
    // this.page.brander.ready = false;
    this.open_page('brander');
  }

  open_stylevote() {
    // if (!this.page.stylevote.contents) {
    //   this.page.stylevote.contents = new PixpairSet(this, 200);
    // }

    // setTimeout(() => { this.open_page('stylevote'); }, 10);
    this.open_page('stylevote');
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
    // window.open('mailto:contact@moiber.com')
    document.location.href = 'mailto:contact@moiber.com';
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

  load_stylelabels() {
    this.stylelabels = new Stylelabels(this);
  }

  load_itemlabels() {
    this.itemlabels = new Itemlabels(this);
  }

  help() {
    this.show_guider = true;
  }

  fix_window_width() {
    setTimeout(() => {
      const w = document.querySelector('#moiber > .window').clientWidth;
      document.documentElement.style.setProperty('--width', w + 'px');
    }, 400);
  }

  release_window_width() {
    setTimeout(() => {
      document.documentElement.style.setProperty('--width', 'min(var(--width-max), 100vw, calc(100vh * 11 / 16))');
    }, 300);
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
    if (this.loaded || this.onloading) {
      return this
    }

    // if (!this.loaded && !this.onloading) {
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
    // }

    return this
  }

  // reload() {
  //   this.loaded = false;
  //   this.onloading = false;
  //   this.load();
  // }

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
    this.type = undefined;
  }

  assign(obj) {
    this.desc = obj.desc;
    this.src = obj.src;
    this.outlink = obj.outlink;
    this.type = obj.type;
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
    // this.voting_record = undefined;
    this.genderlabels = undefined;
    // this.agelabels = undefined;
    this.stylelabels = undefined;
    this.itemlabels = undefined;
    this.styleprofile = {};
    // this.contentwork_result = {};
    this.wallet = undefined;
    this.researched = [];
    this.supports = undefined;
    this.raffles = undefined;
  }

  static init(session, baseobj) {
    const boo = super.init(session, baseobj);
    // Vue.set(session.store.boostore, boo.id, boo);
    return boo
  }

  assign(obj) {
    Object.assign(this, obj);
    this.collections = new Collections(this.session, this.id);
    this.supports = new MySupports(this.session);
    this.raffles = new MyRaffles(this.session);
    this.wallet = new Wallet(obj.wallet, this.session);
    this.signup_check();
    // this.help();
  }

  signup_check() {
    const signupinfo = sessionStorage.getItem('signupinfo');
    if (signupinfo && (this.wallet.baseinfo_inputed==false)) {
      fetch(`/signup/setbase?data=${signupinfo}`)
        .then(res => res.json())
        .then(js => { console.log(js); });

      Object.assign(this.session.user.auth, JSON.parse(signupinfo));
      sessionStorage.removeItem('signupinfo');

      this.wallet.receive('baseinfo_input', this.wallet.amount_baseinfo_input);
      this.wallet.baseinfo_inputed = true;
      alert(`기본정보 입력으로 ${this.wallet.amount_baseinfo_input}P가 지급되었습니다`);
      this.session.help();
    }
  }

  // help() {
  //   if (this.session.user.auth.help) {
  //     this.session.show_guider = true;
  //   }
  // }


  // 10/30/50/70/100
  balancegame_stat_update(amount_add) {
    if ([10,30,50,70,100].includes(this.wallet.amount_daybonus + amount_add)) {
      const is_last = 100 == (this.wallet.amount_daybonus + amount_add);

      fetch('balancegame/stat')
        .then(x => x.json())
        .then(js => {
          if (js.success) {
            console.log(js);
            this.session.balancegame.stat = js.stat;
            this.session.balancegame.stat_updated = true;
            this.session.balancegame.stat_last = is_last;
          }
        });
    }
  }

  stylevote(ipix_pos, ipix_neg, type) {
    if (!this.wallet) {
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
      this.wallet.receive_daybonus('daily_balance_game', (-1) * this.wallet.per_vote);

    } else if (type == 'new') {
      // if (this.session.user.auth.is_superuser) {
        this.balancegame_stat_update(this.wallet.per_vote); // 순서가 바뀌면 안된다
      // }

      this.wallet.receive_daybonus('daily_balance_game', this.wallet.per_vote);
    }

    // if ([10,20,30,40,50,60,70,80,90,100].includes(this.wallet.amount_daybonus)) {
    //   fetch('balancegame/stat')
    //     .then(x => x.json())
    //     .then(js => {
    //       if (js.success) {
    //         console.log(js);
    //         this.session.balancegame.stat = js.stat;
    //         this.session.balancegame.stat_updated = true;
    //       }
    //     });
    // }
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

    this.session.open_texteditor('', '컬렉션 이름을 입력해주세요', 1, txt_done => {
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


class Wallet {
  // types ###
  // 0 checkin_game
  // 1 daily_balance_game
  // 2 daily_collecting
  // 3 research
  // 4 interview
  // 5 welcome
  // 6 baseinfo_input
  // 7 stylelabels_input
  // 8 itemlabels_input
  // 100 support
  // 101 raffle
  // 102 shopping

  constructor(wallet, session) {
    Object.assign(this, wallet);
    this.session = session;
    this.amount_daybonus_max = 100;
    this.per_vote = 1;
    this.per_collect = 1;
    this.per_checkin = 10;
    // this.amount_welcome = 500;
    this.amount_baseinfo_input = 100;
    this.amount_stylelabels_input = 50;
    this.amount_itemlabels_input = 50;
    this.amount_to_levelup = 5000;
  }



  send(type, amount, receiver_id) {
    fetch(`transact?receiver_id=${receiver_id}&type=${type}&amount=${amount}`)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          console.log(js);
        }
      });

    this.amount -= amount;
  }

  receive(type, amount) {
    fetch(`transact?type=${type}&amount=${amount}`)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          console.log(js);
        }
      });

    this.amount += amount;
  }

  receive_daybonus(type, amount) {
    if (amount > 0) {
      amount = Math.min(this.amount_daybonus + amount, this.amount_daybonus_max) - this.amount_daybonus;

      if (amount > 0) {
        this.receive(type, amount);
        this.amount_daybonus += amount;
      }

    } else {
      this.receive(type, amount);
      this.amount_daybonus += amount;
    }
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


class Stylelabel extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/label/style/${baseobj.id}`;
    this.label = undefined;
    this.pix = undefined;
  }
}

class Itemlabel extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/label/item/${baseobj.id}`;
    this.label = undefined;
    this.pix = undefined;
  }
}


// class Checkingame extends Loader {
//   constructor(session, baseobj) {
//     super(session, baseobj);
//     this.url = `/research/checkingame`;
//     this.order = undefined;
//     this.type = undefined;
//     this.gender = undefined;
//     this.preq = undefined;
//     this.question = undefined;
//     this.pix = undefined;
//     this.mc = undefined;
//   }
// }

class Flashgame extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/flashgame/${baseobj.id}`;
    this.type = undefined;
    this.gender = undefined;
    this.text = undefined;
    this.pix = undefined;
    this.reward = undefined;
    this.pub_date = undefined;
    this.published = undefined;
    this.stat = undefined;
    this.answer = undefined;
  }

  // assign(obj) {
  //   Object.assign(this, obj);
  //
  //   const _today = moment(new Date()).format('YYYY-MM-DD');
  //
  //
  // }
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
    this.winner = undefined;
    this.send_requested = false;
  }

  assign(obj) {
    this.item = Item.init(this.session, obj.item);
    this.deduction = obj.deduction;
    this.due = obj.due;
    this.wallet = obj.wallet;
    this.winner = obj.winner;
    this.send_requested = obj.send_requested;
  }

  static init(session, baseobj) {
    if (baseobj.id in session.store.rafflestore) {
      return session.store.rafflestore[baseobj.id]

    } else {
      const raffle = super.init(session, baseobj);
      Vue.set(session.store.rafflestore, raffle.id, raffle);
      return raffle
    }
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
    this.priority = undefined;
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
    this.priority = obj.priority;

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

  static init(session, baseobj) {
    if (baseobj.id in session.store.supportstore) {
      return session.store.supportstore[baseobj.id]

    } else {
      const support = super.init(session, baseobj);
      Vue.set(session.store.supportstore, support.id, support);
      return support
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


class Stylelabels extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Stylelabel;
    this.nloads_init = 20;
    this.ids_url = `/label/istylelabels`;
    this.load_ids();
  }
}

class Itemlabels extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Itemlabel;
    this.nloads_init = 20;
    this.ids_url = `/label/iitemlabels`;
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


class Raffles extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Raffle;
    this.nloads_init = 10;
    this.ids_url = `/raffle/iraffles`;
    this.load_ids();
  }
}


class MySupports extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Support;
    this.nloads_init = 10;
    this.ids_url = `/support/isupports/my`;
    this.load_ids();
  }
}


class MyRaffles extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Raffle;
    this.nloads_init = 10;
    this.ids_url = `/raffle/iraffles/my`;
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


class Flashgames extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Flashgame;
    this.nloads_init = 1;
    this.ids_url = `/flashgame/iflashgames`;
    this.load_ids();
  }
}



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

// class Pixpair extends Multiloader {
//   constructor(session, baseobj) {
//     super(session);
//     this.contentype = Pix;
//     this.ids = baseobj.id;
//     // this.load(2);
//   }
//
//   static build(session, baseobj) {
//     return new this(session, baseobj).load(2)
//   }
// }
//
// class PixpairSet extends Multiloader {
//   constructor(session, n) {
//     super(session);
//     this.contentype = Pixpair;
//     this.nloads_init = 3;
//     this.ids_url = `/pix/ipixs/comb/${n}`;
//     this.load_ids();
//   }
// }

class Pixpair extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Pix;
    this.nloads_init = 2;
    this.ids_url = `/pixpair/ipixs`;
    this.load_ids();
  }
}

class PixpairSet extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Pixpair;
    this.load(1);
  }

  load(n) {
    if (!n) { var n = 1; }
    this.list_onloading = [];

    for (let i = 0; i < n; i++) {
      const content = new this.contentype(this.session);
      this.list.push(content);
      this.list_onloading.push(content);
    };

    return this
  }
}


class Store {
  constructor() {
    this.pixstore = {};
    this.boostore = {};
    this.brandstore = {};
    this.itemstore = {};
    this.supportstore = {};
    this.rafflestore = {};
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

        if (js.mode == 0) {
          this.auth = new Auth(js.user, this.session);

        } else if (js.mode == 1) {
          this.guest = { boo: JSON.parse(js.guestboo) };

        } else {

        }

        // if (js.success) {
        //   this.auth = new Auth(js.user, this.session);
        // }
        //
        // this.guest = { boo: JSON.parse(js.guestboo) };
        this.onloading = false;
      });
  }

  // reload() {
  //   this.auth = undefined;
  //   this.guest = undefined;
  //   this.onloading = true;
  //   this.load();
  // }

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

  // contentvote(postage_id, action) {
  //   if (!this.boo) {
  //     return
  //   }
  //
  //   const feed_act = {};
  //   feed_act[postage_id] = action;
  //   this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);
  //
  //   fetch(`/postage/${postage_id}/contentvote?action=${action}`)
  //     .then(x => x.json())
  //     .then(js => {
  //       console.log(js);
  //     });
  // }


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

  // has_voted_as(postage_id) {
  //   if (!this.boo)
  //     return -1
  //
  //   if (!this.boo.voting_record)
  //     return -1
  //
  //   if (postage_id in this.boo.voting_record) {
  //     return this.boo.voting_record[postage_id]
  //
  //   } else {
  //     return -1
  //   }
  // }

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
    this.cuser = cuser;
    this.id = Number(cuser.id);
    this.name = cuser.name;
    this.gender = cuser.gender==0 ? '남성' : '여성';
    this.birth = cuser.birth;
    this.address = cuser.address;
    this.mobile = cuser.mobile;
    this.mobile_verified = cuser.mobile_verified;
    // this.store = store;
    this.session = session;
    this.email = cuser.email;
    this.is_superuser = cuser.is_superuser;
    this.help = cuser.help;
    this.referal_code = cuser.referal_code;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.build(session, cuser.boo)} : {};
    // this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.build(cuser.boo.id, store)} : {};
    // this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.rebuild(cuser.boo, store, true)} : {};
    this.boos_fully_loaded = false;
    // this.links = cuser.links;
    // this.load_other_boos();
    // this.signup_check();
  }

  reload_boos() {
    this.boos = {};
    setTimeout(() => {
      this.boos = this.cuser.boo ? {[this.cuser.boo_selected]: Boo.build(this.session, this.cuser.boo)} : {};
    }, 10);
  }


  // signup_check() {
  //   const signupinfo = sessionStorage.getItem('signupinfo');
  //   if (signupinfo) {
  //     fetch(`/signup/setbase?data=${signupinfo}`)
  //       .then(res => res.json())
  //       .then(js => { console.log(js); });
  //
  //     Object.assign(this, JSON.parse(signupinfo));
  //     sessionStorage.removeItem('signupinfo');
  //     alert('기본정보 입력으로 100P가 지급되었습니다')
  //   }
  // }

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

  // load_other_boos() {
  //   fetch('/user2/other_boos')
  //     .then(x => x.json())
  //     .then(js => {
  //       if (js.success) {
  //         this.boos = { ...this.boos, ...js.other_boos };
  //         this.boos_fully_loaded = true;
  //       }
  //     })
  // }

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
    // return this.session.store.boostore[this.boo_selected]
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
